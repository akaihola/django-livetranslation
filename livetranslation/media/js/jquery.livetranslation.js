(function($) {

    /* Helpers */

    var nano = function(template, data) {
        // Nano Templates (Tomasz Mazur, Jacek Becela)
        return template.replace(/\{([\w\.]*)\}/g, function (str, key) {
            var keys = key.split("."), value = data[keys.shift()];
            $.each(keys, function () { value = value[this]; });
            return (value === null || value === undefined) ? "" : value;
        });
    };

    var keys = function(obj) {
        // returns the keys of an object as an array
        var result = [];
        $.each(obj, function(key) { result.push(key) });
        return result;
    };

    // DOM IDs for key elements
    var id = {};
    id.prefix = 'livetranslation-';
    id.opener = id.prefix + 'opener';
    id.popup = id.prefix + 'popup';
    id.popupContent = id.popup + '-content';
    id.form = id.popup + '-form';
    id.popupClose = id.popup + '-close';

    // jQuery references to key elements are held in the ``dom`` object
    var dom = {};


    /* Layout */

    function minus5px(index, val) { return parseFloat(val) - 5 + 'px'; }

    var msgstr_css = {'-webkit-box-shadow': '5px 5px 15px',
                      MozBoxShadow: '5px 5px 15px',
                      'box-shadow': '5px 5px 15px',
                      paddingTop: '5px',
                      paddingRight: '5px',
                      paddingBottom: '5px',
                      paddingLeft: '5px',
                      marginTop: minus5px,
                      marginRight: minus5px,
                      marginBottom: minus5px,
                      marginLeft: minus5px}


    /* Pop-up translation form */

    dom.popup = $(nano(
        '<div id="{popup}">' +
            '<form id="{form}">' +
                '<div id="{close}"></div>' +
                '<div id="{content}"></div>' +
                '<input type="submit" value="Save"/>' +
            '</form>' +
        '</div>', {popup: id.popup,
                   form: id.form,
                   close: id.popupClose,
                   content: id.popupContent}));

    dom.popup.showFor = function(msgstr) {
        var msgstr_ofs = msgstr.offset();
        var win = $(window);
        this.show().css({
            top: makeVisible(
                win.scrollTop(), win.height(), 400,
                msgstr_ofs.top + msgstr.height() + 15),
            left: makeVisible(
                win.scrollLeft(), win.width(), 300,
                msgstr_ofs.left)});
        msgstr.getLivetranslationData(function(data) {
            var singular = makePopupSection('singular', data);
            dom.popupContent
                .empty()
                .append(singular);
            if (data.plural) {
                var plural = makePopupSection('plural', data);
                dom.popupContent.append(plural);
            } }); };

    dom.popupContent = $('#' + id.popupContent, dom.popup);

    dom.popupClose = $('#' + id.popupClose, dom.popup)
        .click(function() { dom.popup.hide(); });

    theform = $('#' + id.form, dom.popup).submit(function() {
        $.post('/livetranslation/',
               $(this).serialize());
        return false; });

    // Pop-up helpers

    var makeVisible = function(
        windowOffset, windowSize, popupSize, popupOffset) {
        // returns popupOffset or the largest offset which keeps the whole
        // popup inside the visible area of the page
        return popupOffset + popupSize > windowOffset + windowSize
            ? Math.max(windowOffset + 5, windowOffset + windowSize - popupSize)
            : popupOffset; };

    var makePopupSection = function(typ, data) {
        // Creates the #livetranslation-popup-{singular,plural} sections. Adds
        // the original msgid as a title and msgstrs in different languages as
        // fields.
        var prefix = id.prefix + 'popup-' + typ;

        var fields = $.map(data[typ].msgstrs, function(item) {
            return nano(
                '<label for="{prefix}-{lang}" class="{cls}">{lang}</label>' +
                '<input name="{prefix}-{lang}" type="text" value="{msgstr}"/>',
                {prefix: prefix,
                 lang: item[0],
                 cls: id.prefix + 'lang-' + item[0],
                 msgstr: item[1]}); });

        var section = $(nano(
            '<div id="{prefix}">' +
                '<div id="{prefix}-msgid">{msgid}</div>' +
                '<input type="hidden" name="{prefix}-msgid"' +
                ' value="{msgid}"/>' +
                '{fields}' +
            '</div>',
            {prefix: prefix,
             msgid: data[typ].msgid,
             fields: fields.join('')}));
        return section; };


    /* Icon for opening pop-up translation form */

    dom.opener = $('<div/>')
        .attr('id', id.opener)
        .click(function() {
            var msgstr = $.livetranslate.data.current_msgstr;
            dom.popup.showFor(msgstr);
        });


    /* Attach elements to page after page has been loaded */

    $(function() {
        dom.opener.appendTo('body')
        dom.popup.appendTo('body');
    });


    /* Global data object */

    $.livetranslate = {
        data: {current_msgstr: $()}
    };


    /* jQuery plugin methods */

    $.fn.livetranslate = function(msgid, msgid_plural) {
        this.data('msgid', msgid);
        this.data('msgid_plural', msgid_plural);
        return this.each(function() {
            var elem = $(this);
            var old_css = {};
            var new_css = {};
            $.each(msgstr_css, function(attr, new_val) {
                var val = elem.css(attr);
                if (val) {
                    old_css[attr] = val == 'none' ? '0 0' : val;
                    new_css[attr] = new_val;
                }
            });

            $(this).hover(
                function() {
                    var data = $.livetranslate.data;
                    if (data.current_msgstr.length && data.current_msgstr[0] != this) {
                        data.current_msgstr.trigger(
                            'livetranslation-deactivate', [0]);
                    }
                    var elem = $(this);
                    elem.stop(true, true).css(old_css).css(new_css);
                    var ofs = elem.offset();
                    var icon_ofs = {left: ofs.left + elem.width() - 10,
                                    top: ofs.top - 20};
                    if (icon_ofs.top < 0)
                        icon_ofs.top = ofs.top + elem.height() + 10;
                    data.current_msgstr = elem;
                    dom.opener.stop(true, false)
                              .offset(icon_ofs)
                              .fadeTo(100, 1.0);
                },
                function() {
                    $(this).trigger('livetranslation-deactivate', [5000]);
                    dom.opener.stop(true, false)
                              .delay(5000)
                              .fadeOut(100);
                });

            $(this).bind('livetranslation-deactivate', function(e, delay) {
                $(this).stop(true, false)
                       .delay(delay)
                       .animate(old_css, 100);
            });
        });
    };

    $.fn.getLivetranslationData = function(callback) {
        $.get('/livetranslation/',
              {msgid: this.data('msgid'),
               msgid_plural: this.data('msgid_plural')},
              callback);
    };

})(jQuery);
