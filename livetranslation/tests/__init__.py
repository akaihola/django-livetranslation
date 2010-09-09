from livetranslation.tests.forms_tests import Forms_Tests
from livetranslation.tests.gettext_tests import Gettext_Tests
from livetranslation.tests.markup_tests import (
    GetTranslationItemMarkup_Tests,
    MarkTranslation_Tests,
    GetAttributeTranslationRegex_Tests,
    MarkupToRegex_Tests,
    MarkupRegex_Tests,
    ReplaceAttributeTranslation_Tests,
    RenderAttributeTranslations_Tests,
    ReplaceContentTranslation_Tests,
    RenderContentTranslations_Tests)
from livetranslation.tests.middleware_tests import (
    ProcessJquerySetting_Tests,
    FindJqueryLink_Tests,
    InsertJqueryLink_Tests,
    LiveTranslationMiddleware_Tests)
from livetranslation.tests.templatetag_tests import Trans_Tests
from livetranslation.tests.translation_tests import (
    GetAllTranslations_Tests, PoFileSession_Tests)
from livetranslation.tests.views_tests import (GetTranslations_GET_Tests,
                                               GetTranslations_POST_Tests)
