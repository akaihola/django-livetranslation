def extract_form_data(post):
    prefix = 'livetranslation-popup-'
    data = {}

    def get_post_var(varname):
        return post.get('%s%s' % (prefix, varname))

    for full_varname, value in post.items():
        if full_varname.startswith(prefix):
            number, code = full_varname[len(prefix):].split('-')
            number_data = data.setdefault(number, {})
            if code == 'msgid':
                number_data['msgid'] = value
            else:
                msgstrs = number_data.setdefault('msgstrs', [])
                msgstrs.append((code, value))

    return data
