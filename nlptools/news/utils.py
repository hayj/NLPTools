
from enum import Enum

TOKEN_TYPE = Enum("TOKEN_TYPE", "int float alpha_strict alpha_accent alpha_num mixed_strict mixed price unknown punct1 punct2 atreply hashtag known_emoji emoji url netloc email none quote currency social function")

TOKEN_TYPE_EXAMPLES = \
{
	TOKEN_TYPE.int: ["84", "0", "1111111111111111111111111", "0"],
	TOKEN_TYPE.float: ["0.0", "0.0003", "1111111111111111111111111.0"],
	TOKEN_TYPE.alpha_strict: ["a", "aUfRCc", "lkYfd", "pojhjbdf"],
	TOKEN_TYPE.alpha_accent: ["à", "àlo", "élOO"],
	TOKEN_TYPE.alpha_num: ["op91"],
	TOKEN_TYPE.mixed_strict: ["AAA-bbb", "aaaa-bbb", "U.S.A.", "Mr.", 'aa.bb.ccc'],
	TOKEN_TYPE.mixed: ["aaaa-", "_aaaa", 'élo_u', 'àlo_01'],
	TOKEN_TYPE.price: ["10.0€", "$20", "$0.888888"],
	TOKEN_TYPE.unknown: ["10,000", "10:45", "10:45am", "pm10:45", "10.45.30", "19/12/30", "@u€", "#aaa_[", "e" * 100, "µ", "rr§rr", "1" * 100, ".0", "0.", "10/", "/00", "^^", "(((", 'http//uyhf.com', 'iojf@iujsdf'],
	TOKEN_TYPE.punct1: [',', ')', '...', ';', '-', '!', ':', '?', '.', '('],
	TOKEN_TYPE.punct2: list("<>[]|{}~^_/*—"),
	TOKEN_TYPE.atreply: ["@uhFvd", "@uhFvd_Yfvvd076", "@uhFvd-Yfvvd076"],
	TOKEN_TYPE.hashtag: ["#uhFvd", "#uhFvd_Yfvvd076", "#uhFvd-Yfvvd076"],
	TOKEN_TYPE.known_emoji: ['😑', '😠', '🙆', '😂', '😫', '😄', '😰', '💗', '👋', '😽', '😉', '😳', '🙌', '😤', '😶', '😢', '😖', '💔', '😐', '😁', '😓', '😜', '😵', '😃', '😇', '🙅', '😍', '😱', '😲', '😡', '😼', '😒', '😈'],
	TOKEN_TYPE.emoji: [],
	TOKEN_TYPE.url: ['http://ipezrf.com', 'https://aa.net', 'ftp://aa.tt'],
	TOKEN_TYPE.netloc: ['ipezrf.com', 'aa.net', 'aa.bb.lol'],
	TOKEN_TYPE.email: ['iojf@iujsdf.fr', 'iojf@iujsdf.ee'],
	TOKEN_TYPE.none: [None],
	TOKEN_TYPE.quote: list("'\""),
	TOKEN_TYPE.currency: list("$€£¥"),
	TOKEN_TYPE.social: list("@#"),
	TOKEN_TYPE.function: list("&%+="),
}


netLocEnd3 = {'.biz', '.xxx', '.com', '.int', '.org', '.pro', '.cat', '.mil', '.edu', '.tel', '.gov', '.net', '.lol', '.xyz'}
netLocEnd2 = {'.bh', '.hr', '.gr', '.mk', '.ng', '.sd', '.hu', '.si', '.mx', '.ge', '.al', '.ki', '.fj', '.cg', '.at', '.sg', '.uy', '.wf', '.ai', '.km', '.is', '.bd', '.pl', '.ba', '.kn', '.ph', '.pn', '.vi', '.jm', '.bw', '.sx', '.lu', '.yt', '.eu', '.tl', '.sm', '.au', '.bz', '.cu', '.ro', '.tv', '.ac', '.kw', '.mg', '.co', '.hm', '.vu', '.pk', '.ar', '.bf', '.bv', '.va', '.ga', '.me', '.ch', '.mq', '.bs', '.lk', '.iq', '.nu', '.td', '.gf', '.na', '.gi', '.lv', '.cv', '.zm', '.tr', '.in', '.dz', '.gh', '.bj', '.us', '.et', '.cm', '.ua', '.su', '.gw', '.ir', '.lc', '.pe', '.gb', '.ck', '.lb', '.my', '.bb', '.dm', '.gt', '.mt', '.sl', '.ye', '.bo', '.gg', '.er', '.mu', '.tm', '.af', '.tp', '.ms', '.np', '.kr', '.th', '.sn', '.dj', '.mp', '.pr', '.za', '.gn', '.ve', '.sr', '.bn', '.mn', '.gq', '.sb', '.it', '.li', '.jp', '.fk', '.ma', '.io', '.ni', '.cc', '.sv', '.mv', '.je', '.sh', '.sy', '.az', '.gs', '.vc', '.sj', '.zw', '.eg', '.uz', '.tg', '.mz', '.sc', '.tz', '.tf', '.sk', '.de', '.py', '.uk', '.ec', '.im', '.ne', '.pf', '.by', '.bm', '.pa', '.pt', '.rs', '.ru', '.so', '.cn', '.tn', '.mm', '.br', '.kg', '.mr', '.ax', '.vg', '.ky', '.ke', '.mw', '.hn', '.gp', '.la', '.ls', '.to', '.st', '.ad', '.an', '.il', '.lr', '.bi', '.fo', '.kh', '.mc', '.md', '.tt', '.sa', '.gy', '.be', '.ps', '.gm', '.no', '.dd', '.fi', '.cs', '.pw', '.nc', '.kp', '.om', '.ss', '.cf', '.bg', '.cl', '.pg', '.pm', '.ja', '.mo', '.ae', '.es', '.ee', '.am', '.jo', '.cx', '.re', '.tj', '.ws', '.id', '.gl', '.gd', '.lt', '.aw', '.ug', '.ie', '.se', '.nl', '.ca', '.gu', '.cz', '.mh', '.sz', '.cy', '.yu', '.ag', '.qa', '.vn', '.tc', '.kz', '.tk', '.aq', '.cd', '.nz', '.do', '.tw', '.nr', '.rw', '.ao', '.fr', '.as', '.nf', '.hk', '.bt', '.ht', '.ci', '.eh', '.fm', '.cr', '.ml', '.ly', '.dk'}




