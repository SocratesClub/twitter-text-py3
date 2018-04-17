#  encoding=utf-8

# A collection of regular expressions for parsing Tweet text. The regular expression
# list is frozen at load time to ensure immutability. These reular expressions are
# used throughout the Twitter classes. Special care has been taken to make
# sure these reular expressions work with Tweets in all languages.
import re, string
from functools import reduce

REGEXEN = {} # :nodoc:

def regex_range(start, end = None):
    if end:
        return u'%s-%s' % (chr(start), chr(end))
    else:
        return u'%s' % chr(start)

# Space is more than %20, U+3000 for example is the full-width space used with Kanji. Provide a short-hand
# to access both the list of characters and a pattern suitible for use with String#split
#  Taken from: ActiveSupport::Multibyte::Handlers::UTF8Handler::UNICODE_WHITESPACE
UNICODE_SPACES = []
for space in reduce(lambda x,y: list(x) + y if type(y) == list else list(x) + [y], [
        [0x0009, 0x000D],  # White_Space # Cc   [5] <control-0009>..<control-000D>
        0x0020,                 # White_Space # Zs       SPACE
        0x0085,                 # White_Space # Cc       <control-0085>
        0x00A0,                 # White_Space # Zs       NO-BREAK SPACE
        0x1680,                 # White_Space # Zs       OGHAM SPACE MARK
        0x180E,                 # White_Space # Zs       MONGOLIAN VOWEL SEPARATOR
        [0x2000, 0x200A],  # White_Space # Zs  [11] EN QUAD..HAIR SPACE
        0x2028,                 # White_Space # Zl       LINE SEPARATOR
        0x2029,                 # White_Space # Zp       PARAGRAPH SEPARATOR
        0x202F,                 # White_Space # Zs       NARROW NO-BREAK SPACE
        0x205F,                 # White_Space # Zs       MEDIUM MATHEMATICAL SPACE
        0x3000,                 # White_Space # Zs       IDEOGRAPHIC SPACE
    ]):
    UNICODE_SPACES.append(chr(space))
REGEXEN['spaces'] = re.compile(u''.join(UNICODE_SPACES))

# Characters not allowed in Tweets
INVALID_CHARACTERS  =   [
    0xFFFE, 0xFEFF,                         # BOM
    0xFFFF,                                 # Special
    0x202A, 0x202B, 0x202C, 0x202D, 0x202E, # Directional change
]
REGEXEN['invalid_control_characters']   =   [chr(x) for x in INVALID_CHARACTERS]

REGEXEN['list_name'] = re.compile(u'^[a-zA-Z][a-zA-Z0-9_\-\u0080-\u00ff]{0,24}$')

# Latin accented characters
# Excludes 0xd7 from the range (the multiplication sign, confusable with "x").
# Also excludes 0xf7, the division sign
LATIN_ACCENTS = [
    regex_range(0x00c0, 0x00d6),
    regex_range(0x00d8, 0x00f6),
    regex_range(0x00f8, 0x00ff),
    regex_range(0x0100, 0x024f),
    regex_range(0x0253, 0x0254),
    regex_range(0x0256, 0x0257),
    regex_range(0x0259),
    regex_range(0x025b),
    regex_range(0x0263),
    regex_range(0x0268),
    regex_range(0x026f),
    regex_range(0x0272),
    regex_range(0x0289),
    regex_range(0x028b),
    regex_range(0x02bb),
    regex_range(0x0300, 0x036f),
    regex_range(0x1e00, 0x1eff),
]
REGEXEN['latin_accents'] = re.compile(u''.join(LATIN_ACCENTS), re.IGNORECASE | re.UNICODE)
LATIN_ACCENTS = u''.join(LATIN_ACCENTS)

RTL_CHARACTERS = ''.join([
    regex_range(0x0600,0x06FF),
    regex_range(0x0750,0x077F),
    regex_range(0x0590,0x05FF),
    regex_range(0xFE70,0xFEFF)
])

NON_LATIN_HASHTAG_CHARS = ''.join([
    # Cyrillic (Russian, Ukrainian, etc.)
    regex_range(0x0400, 0x04ff), # Cyrillic
    regex_range(0x0500, 0x0527), # Cyrillic Supplement
    regex_range(0x2de0, 0x2dff), # Cyrillic Extended A
    regex_range(0xa640, 0xa69f), # Cyrillic Extended B
    regex_range(0x0591, 0x05bf), # Hebrew
    regex_range(0x05c1, 0x05c2),
    regex_range(0x05c4, 0x05c5),
    regex_range(0x05c7),
    regex_range(0x05d0, 0x05ea),
    regex_range(0x05f0, 0x05f4),
    regex_range(0xfb12, 0xfb28), # Hebrew Presentation Forms
    regex_range(0xfb2a, 0xfb36),
    regex_range(0xfb38, 0xfb3c),
    regex_range(0xfb3e),
    regex_range(0xfb40, 0xfb41),
    regex_range(0xfb43, 0xfb44),
    regex_range(0xfb46, 0xfb4f),
    regex_range(0x0610, 0x061a), # Arabic
    regex_range(0x0620, 0x065f),
    regex_range(0x066e, 0x06d3),
    regex_range(0x06d5, 0x06dc),
    regex_range(0x06de, 0x06e8),
    regex_range(0x06ea, 0x06ef),
    regex_range(0x06fa, 0x06fc),
    regex_range(0x06ff),
    regex_range(0x0750, 0x077f), # Arabic Supplement
    regex_range(0x08a0),         # Arabic Extended A
    regex_range(0x08a2, 0x08ac),
    regex_range(0x08e4, 0x08fe),
    regex_range(0xfb50, 0xfbb1), # Arabic Pres. Forms A
    regex_range(0xfbd3, 0xfd3d),
    regex_range(0xfd50, 0xfd8f),
    regex_range(0xfd92, 0xfdc7),
    regex_range(0xfdf0, 0xfdfb),
    regex_range(0xfe70, 0xfe74), # Arabic Pres. Forms B
    regex_range(0xfe76, 0xfefc),
    regex_range(0x200c, 0x200c), # Zero-Width Non-Joiner
    regex_range(0x0e01, 0x0e3a), # Thai
    regex_range(0x0e40, 0x0e4e), # Hangul (Korean)
    regex_range(0x1100, 0x11ff), # Hangul Jamo
    regex_range(0x3130, 0x3185), # Hangul Compatibility Jamo
    regex_range(0xA960, 0xA97F), # Hangul Jamo Extended-A
    regex_range(0xAC00, 0xD7AF), # Hangul Syllables
    regex_range(0xD7B0, 0xD7FF), # Hangul Jamo Extended-B
    regex_range(0xFFA1, 0xFFDC)  # Half-width Hangul
])

CJ_HASHTAG_CHARACTERS = ''.join([
    regex_range(0x30A1, 0x30FA), regex_range(0x30FC, 0x30FE), # Katakana (full-width)
    regex_range(0xFF66, 0xFF9F), # Katakana (half-width)
    regex_range(0xFF10, 0xFF19), regex_range(0xFF21, 0xFF3A), regex_range(0xFF41, 0xFF5A), # Latin (full-width)
    regex_range(0x3041, 0x3096), regex_range(0x3099, 0x309E), # Hiragana
    regex_range(0x3400, 0x4DBF), # Kanji (CJK Extension A)
    regex_range(0x4E00, 0x9FFF), # Kanji (Unified)
])

try:
    CJ_HASHTAG_CHARACTERS = ''.join([
        CJ_HASHTAG_CHARACTERS,
        regex_range(0x20000, 0x2A6DF), # Kanji (CJK Extension B)
        regex_range(0x2A700, 0x2B73F), # Kanji (CJK Extension C)
        regex_range(0x2B740, 0x2B81F), # Kanji (CJK Extension D)
        regex_range(0x2F800, 0x2FA1F), regex_range(0x3003), regex_range(0x3005), regex_range(0x303B) # Kanji (CJK supplement)
    ])
except ValueError:
    # this is a narrow python build so these extended Kanji characters won't work
    pass

PUNCTUATION_CHARS = u'!"#$%&\'()*+,-./:;<=>?@\[\]^_\`{|}~'
SPACE_CHARS = u" \t\n\x0B\f\r"
CTRL_CHARS = u"\x00-\x1F\x7F"

# A hashtag must contain latin characters, numbers and underscores, but not all numbers.
HASHTAG_ALPHA = u'[a-z_%s]' % (LATIN_ACCENTS + NON_LATIN_HASHTAG_CHARS + CJ_HASHTAG_CHARACTERS)
HASHTAG_ALPHANUMERIC = u'[a-z0-9_%s]' % (LATIN_ACCENTS + NON_LATIN_HASHTAG_CHARS + CJ_HASHTAG_CHARACTERS)
HASHTAG_BOUNDARY = u'\A|\z|\[|[^&a-z0-9_%s]' % (LATIN_ACCENTS + NON_LATIN_HASHTAG_CHARS + CJ_HASHTAG_CHARACTERS)

HASHTAG = re.compile(u'(%s)(#|＃)(%s*%s%s*)' % (HASHTAG_BOUNDARY, HASHTAG_ALPHANUMERIC, HASHTAG_ALPHA, HASHTAG_ALPHANUMERIC), re.IGNORECASE)

REGEXEN['valid_hashtag'] = HASHTAG
REGEXEN['end_hashtag_match'] = re.compile(u'\A(?:[#＃]|:\/\/)', re.IGNORECASE | re.UNICODE)
REGEXEN['numeric_only'] = re.compile(u'^[\d]+$')

REGEXEN['valid_mention_preceding_chars'] = re.compile(r'(?:[^a-zA-Z0-9_!#\$%&*@＠]|^|RT:?)')
REGEXEN['at_signs'] = re.compile(u'[@＠]')
REGEXEN['valid_mention_or_list'] = re.compile(
    u'(%s)' % REGEXEN['valid_mention_preceding_chars'].pattern + #.decode('utf-8') +   # preceding character
    u'(%s)' % REGEXEN['at_signs'].pattern +                                        # at mark
    u'([a-zA-Z0-9_]{1,20})' +                                                      # screen name
    u'(\/[a-zA-Z][a-zA-Z0-9_\-]{0,24})?'                                           # list (optional)
)
REGEXEN['valid_reply'] = re.compile(u'^(?:[%s])*%s([a-zA-Z0-9_]{1,20})' % (REGEXEN['spaces'].pattern, REGEXEN['at_signs'].pattern), re.IGNORECASE | re.UNICODE)
 # Used in Extractor for final filtering
REGEXEN['end_mention_match'] = re.compile(u'\A(?:%s|[%s]|:\/\/)' % (REGEXEN['at_signs'].pattern, REGEXEN['latin_accents'].pattern), re.IGNORECASE | re.UNICODE)

# URL related hash regex collection
REGEXEN['valid_url_preceding_chars'] = re.compile(u'(?:[^A-Z0-9@＠$#＃%s]|^)' % u''.join(REGEXEN['invalid_control_characters']), re.IGNORECASE | re.UNICODE)
REGEXEN['invalid_url_without_protocol_preceding_chars'] = re.compile(u'[-_.\/]$')
DOMAIN_VALID_CHARS = u'[^%s%s%s%s%s]' % (PUNCTUATION_CHARS, SPACE_CHARS, CTRL_CHARS, u''.join(REGEXEN['invalid_control_characters']), u''.join(UNICODE_SPACES))
REGEXEN['valid_subdomain'] = re.compile(u'(?:(?:%s(?:[_-]|%s)*)?%s\.)' % (DOMAIN_VALID_CHARS, DOMAIN_VALID_CHARS, DOMAIN_VALID_CHARS), re.IGNORECASE | re.UNICODE)
REGEXEN['valid_domain_name'] = re.compile(u'(?:(?:%s(?:[-]|%s)*)?%s\.)' % (DOMAIN_VALID_CHARS, DOMAIN_VALID_CHARS, DOMAIN_VALID_CHARS), re.IGNORECASE | re.UNICODE)
REGEXEN['valid_gTLD'] = re.compile(u'(?:(?:aero|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|xxx)(?=[^0-9a-z]|$))', re.IGNORECASE | re.UNICODE)
REGEXEN['valid_ccTLD'] = re.compile(u'(?:(?:ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|za|zm|zw)(?=[^0-9a-z]|$))', re.IGNORECASE | re.UNICODE)
REGEXEN['valid_punycode'] = re.compile(u'(?:xn--[0-9a-z]+)', re.IGNORECASE | re.UNICODE)

REGEXEN['valid_domain'] = re.compile(u'(?:%s*%s(?:%s|%s|%s))' % (REGEXEN['valid_subdomain'].pattern, REGEXEN['valid_domain_name'].pattern, REGEXEN['valid_gTLD'].pattern, REGEXEN['valid_ccTLD'].pattern, REGEXEN['valid_punycode'].pattern), re.IGNORECASE | re.UNICODE)

# This is used in Extractor
REGEXEN['valid_ascii_domain'] = re.compile(u'(?:(?:[A-Za-z0-9\-_]|[%s])+\.)+(?:%s|%s|%s)' % (REGEXEN['latin_accents'].pattern, REGEXEN['valid_gTLD'].pattern, REGEXEN['valid_ccTLD'].pattern, REGEXEN['valid_punycode'].pattern), re.IGNORECASE | re.UNICODE)

# This is used in Extractor for stricter t.co URL extraction
REGEXEN['valid_tco_url'] = re.compile(u'^https?:\/\/t\.co\/[a-z0-9]+', re.IGNORECASE | re.UNICODE)

# This is used in Extractor to filter out unwanted URLs.
REGEXEN['invalid_short_domain'] = re.compile(u'\A%s%s\Z' % (REGEXEN['valid_domain_name'].pattern, REGEXEN['valid_ccTLD'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['valid_port_number'] = re.compile(u'[0-9]+')

REGEXEN['valid_general_url_path_chars'] = re.compile(u"[a-z0-9!\*';:=\+\,\.\$\/%%#\[\]\-_~&|@%s]" % LATIN_ACCENTS, re.IGNORECASE | re.UNICODE)
# Allow URL paths to contain balanced parens
#  1. Used in Wikipedia URLs like /Primer_(film)
#  2. Used in IIS sessions like /S(dfd346)/
REGEXEN['valid_url_balanced_parens'] = re.compile(u'\(%s+\)' % REGEXEN['valid_general_url_path_chars'].pattern, re.IGNORECASE | re.UNICODE)
# Valid end-of-path chracters (so /foo. does not gobble the period).
#   1. Allow =&# for empty URL parameters and other URL-join artifacts
REGEXEN['valid_url_path_ending_chars'] = re.compile(u'[a-z0-9=_#\/\+\-%s]|(?:%s)' % (LATIN_ACCENTS, REGEXEN['valid_url_balanced_parens'].pattern), re.IGNORECASE | re.UNICODE)
REGEXEN['valid_url_path'] = re.compile(u'(?:(?:%s*(?:%s %s*)*%s)|(?:%s+\/))' % (REGEXEN['valid_general_url_path_chars'].pattern, REGEXEN['valid_url_balanced_parens'].pattern, REGEXEN['valid_general_url_path_chars'].pattern, REGEXEN['valid_url_path_ending_chars'].pattern, REGEXEN['valid_general_url_path_chars'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['valid_url_query_chars'] = re.compile(u"[a-z0-9!?\*'\(\);:&=\+\$\/%#\[\]\-_\.,~|@]", re.IGNORECASE | re.UNICODE)
REGEXEN['valid_url_query_ending_chars'] = re.compile(u'[a-z0-9_&=#\/]', re.IGNORECASE | re.UNICODE)
REGEXEN['valid_url'] = re.compile(u'((%s)((https?:\/\/)?(%s)(?::(%s))?(/%s*)?(\?%s*%s)?))' % (
    REGEXEN['valid_url_preceding_chars'].pattern,
    REGEXEN['valid_domain'].pattern,
    REGEXEN['valid_port_number'].pattern,
    REGEXEN['valid_url_path'].pattern,
    REGEXEN['valid_url_query_chars'].pattern,
    REGEXEN['valid_url_query_ending_chars'].pattern
), re.IGNORECASE | re.UNICODE)
#   Matches
#   $1 total match
#   $2 Preceeding chracter
#   $3 URL
#   $4 Protocol (optional)
#   $5 Domain(s)
#   $6 Port number (optional)
#   $7 URL Path and anchor
#   $8 Query String

REGEXEN['cashtag'] = re.compile(u'[a-z]{1,6}(?:[._][a-z]{1,2})?', re.IGNORECASE)
REGEXEN['valid_cashtag'] = re.compile(u'(^|[%s])(\$|＄|﹩)(%s)(?=$|\s|[%s])' % (REGEXEN['spaces'].pattern, REGEXEN['cashtag'].pattern, PUNCTUATION_CHARS), re.IGNORECASE)

# These URL validation pattern strings are based on the ABNF from RFC 3986
REGEXEN['validate_url_unreserved'] = re.compile(u'[a-z0-9\-._~]', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_pct_encoded'] = re.compile(u'(?:%[0-9a-f]{2})', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_sub_delims'] = re.compile(u"[!$&'()*+,;=]", re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_pchar'] = re.compile(u'(?:%s|%s|%s|[:\|@])' % (REGEXEN['validate_url_unreserved'].pattern, REGEXEN['validate_url_pct_encoded'].pattern, REGEXEN['validate_url_sub_delims'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_scheme'] = re.compile(u'(?:[a-z][a-z0-9+\-.]*)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_userinfo'] = re.compile(u'(?:%s|%s|%s|:)*' % (REGEXEN['validate_url_unreserved'].pattern, REGEXEN['validate_url_pct_encoded'].pattern, REGEXEN['validate_url_sub_delims'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_dec_octet'] = re.compile(u'(?:[0-9]|(?:[1-9][0-9])|(?:1[0-9]{2})|(?:2[0-4][0-9])|(?:25[0-5]))', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_ipv4'] = re.compile(u'(?:%s(?:\.%s){3})' % (REGEXEN['validate_url_dec_octet'].pattern, REGEXEN['validate_url_dec_octet'].pattern), re.IGNORECASE | re.UNICODE)

# Punting on real IPv6 validation for now
REGEXEN['validate_url_ipv6'] = re.compile(u'(?:\[[a-f0-9:\.]+\])', re.IGNORECASE | re.UNICODE)

# Also punting on IPvFuture for now
REGEXEN['validate_url_ip'] = re.compile(u'(?:%s|%s)' % (REGEXEN['validate_url_ipv4'].pattern, REGEXEN['validate_url_ipv6'].pattern), re.IGNORECASE | re.UNICODE)

# This is more strict than the rfc specifies
REGEXEN['validate_url_subdomain_segment'] = re.compile(u'(?:[a-z0-9](?:[a-z0-9_\-]*[a-z0-9])?)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_domain_segment'] = re.compile(u'(?:[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_domain_tld'] = re.compile(u'(?:[a-z](?:[a-z0-9\-]*[a-z0-9])?)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_domain'] = re.compile(u'(?:(?:%s\.)*(?:%s\.)%s)' % (REGEXEN['validate_url_subdomain_segment'].pattern, REGEXEN['validate_url_domain_segment'].pattern, REGEXEN['validate_url_domain_tld'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_host'] = re.compile(u'(?:%s|%s)' % (REGEXEN['validate_url_ip'].pattern, REGEXEN['validate_url_domain'].pattern), re.IGNORECASE | re.UNICODE)

# Unencoded internationalized domains - this doesn't check for invalid UTF-8 sequences
REGEXEN['validate_url_unicode_subdomain_segment'] = re.compile(u'(?:(?:[a-z0-9]|[^\x00-\x7f])(?:(?:[a-z0-9_\-]|[^\x00-\x7f])*(?:[a-z0-9]|[^\x00-\x7f]))?)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_unicode_domain_segment'] = re.compile(u'(?:(?:[a-z0-9]|[^\x00-\x7f])(?:(?:[a-z0-9\-]|[^\x00-\x7f])*(?:[a-z0-9]|[^\x00-\x7f]))?)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_unicode_domain_tld'] = re.compile(u'(?:(?:[a-z]|[^\x00-\x7f])(?:(?:[a-z0-9\-]|[^\x00-\x7f])*(?:[a-z0-9]|[^\x00-\x7f]))?)', re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_unicode_domain'] = re.compile(u'(?:(?:%s\.)*(?:%s\.)%s)' % (REGEXEN['validate_url_unicode_subdomain_segment'].pattern, REGEXEN['validate_url_unicode_domain_segment'].pattern, REGEXEN['validate_url_unicode_domain_tld'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_unicode_host'] = re.compile(u'(?:%s|%s)' % (REGEXEN['validate_url_ip'].pattern, REGEXEN['validate_url_unicode_domain'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_port'] = re.compile(u'[0-9]{1,5}')

REGEXEN['validate_url_unicode_authority'] = re.compile(u'(?:(%s)@)?(%s)(?::(%s))?' % (REGEXEN['validate_url_userinfo'].pattern, REGEXEN['validate_url_unicode_host'].pattern, REGEXEN['validate_url_port'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_authority'] = re.compile(u'(?:(%s)@)?(%s)(?::(%s))?' % (REGEXEN['validate_url_userinfo'].pattern, REGEXEN['validate_url_host'].pattern, REGEXEN['validate_url_port'].pattern), re.IGNORECASE | re.UNICODE)

REGEXEN['validate_url_path'] = re.compile(u'(/%s*)*' % REGEXEN['validate_url_pchar'].pattern, re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_query'] = re.compile(u'(%s|/|\?)*' % REGEXEN['validate_url_pchar'].pattern, re.IGNORECASE | re.UNICODE)
REGEXEN['validate_url_fragment'] = re.compile(u'(%s|/|\?)*' % REGEXEN['validate_url_pchar'].pattern, re.IGNORECASE | re.UNICODE)

# Modified version of RFC 3986 Appendix B
REGEXEN['validate_url_unencoded'] = re.compile(u'\A(?:([^:/?#]+)://)?([^/?#]*)([^?#]*)(?:\?([^#]*))?(?:\#(.*))?\Z', re.IGNORECASE | re.UNICODE)

REGEXEN['rtl_chars'] = re.compile(u'[%s]' % RTL_CHARACTERS, re.IGNORECASE | re.UNICODE)
