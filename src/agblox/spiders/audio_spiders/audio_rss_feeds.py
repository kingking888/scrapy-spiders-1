"""Classes for initiating RSS feeds spiders."""

from agblox.spiders.audio_spiders.rss_generic_audio_spider import RSSAudioSpider


class MotleyFoolSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://fool.libsyn.com/rss."""

    name: str = "motleyfool"
    url: str = "https://fool.libsyn.com/rss"
    host_header = "fool.libsyn.com"


class ArkInvestSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://ark-invest.com/podcast."""

    name: str = "arkinvest"
    url: str = "https://ark-invest.com/podcast"
    host_header = "ark-invest.com"


class PivotSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.megaphone.fm/pivot."""

    name: str = "pivot"
    url: str = "https://feeds.megaphone.fm/pivot"
    host_header = "feeds.megaphone.fm"


class ChitChatMoneySpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.megaphone.fm/ccmm6330445662."""

    name: str = "chitchatmoney"
    url: str = "https://feeds.megaphone.fm/ccmm6330445662"
    host_header = "feeds.megaphone.fm"


class BusinessDailySpider(RSSAudioSpider):
    """Spider class for RSS feed: https://podcasts.files.bbci.co.uk/p002vsxs.rss."""

    name: str = "businessdaily"
    url: str = "https://podcasts.files.bbci.co.uk/p002vsxs.rss"
    host_header = "podcasts.files.bbci.co.uk"


class FtnewsbriefingSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://rss.acast.com/ftnewsbriefing."""

    name: str = "ftnewsbriefing"
    url: str = "https://rss.acast.com/ftnewsbriefing"
    host_header = "rss.acast.com"


class MadmoneySpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.simplecast.com/TkQfZXMD."""

    name: str = "madmoney"
    url: str = "https://feeds.simplecast.com/TkQfZXMD"
    host_header = "feeds.simplecast.com"


class RichdadSpider(RSSAudioSpider):
    """Spider class for RSS feed: http://simmy.port0.org/podcast/feeds/the_rich_dad_poor_dad.xml."""

    name: str = "richdad"
    url: str = "http://simmy.port0.org/podcast/feeds/the_rich_dad_poor_dad.xml"
    host_header = "simmy.port0.org"


class InvestorsSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://rss.art19.com/the-investors-podcast."""

    name: str = "investors"
    url: str = "https://rss.art19.com/the-investors-podcast"
    host_header = "rss.art19.com"


class FreshinvestSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://rss.art19.com/fresh-invest."""

    name: str = "freshinvest"
    url: str = "https://rss.art19.com/fresh-invest"
    host_header = "rss.art19.com"


class FastmoneySpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.feedburner.com/CnbcsfastMoney."""

    # TODO: Try to use Bozo feed: https://feedparser.readthedocs.io/en/latest/bozo.html

    name: str = "fastmoney"
    url: str = "https://feeds.feedburner.com/CnbcsfastMoney"
    host_header = "feeds.feedburner.com"


class InvestLikeTheBestSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://anchor.fm/s/af18aec/podcast/rss."""

    name: str = "invest_like_the_best"
    url: str = "https://anchor.fm/s/af18aec/podcast/rss"
    host_header = "anchor.fm"


class SchiffradioSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://www.schiffradio.com/feed/podcast/."""

    name: str = "schiffradio"
    url: str = "https://www.schiffradio.com/feed/podcast/"
    host_header = "www.schiffradio.com"


class InvestedSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.megaphone.fm/PPY1133394899."""

    name: str = "invested"
    url: str = "https://feeds.megaphone.fm/PPY1133394899"
    host_header = "feeds.megaphone.fm"


class AnimalspiritsSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://animalspiritspod.libsyn.com/rss."""

    name: str = "animalspirits"
    url: str = "https://animalspiritspod.libsyn.com/rss"
    host_header = "animalspiritspod.libsyn.com"


class PlanetmoneySpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.npr.org/510289/podcast.xml."""

    name: str = "planetmoney"
    url: str = "https://feeds.npr.org/510289/podcast.xml"
    host_header = "feeds.npr.org"


class NotboringSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://anchor.fm/s/16186c88/podcast/rss."""

    name: str = "notboring"
    url: str = "https://anchor.fm/s/16186c88/podcast/rss"
    host_header = "anchor.fm"


class QuantcastSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.soundcloud.com/users/soundcloud:users:387150302/sounds.rss."""

    name: str = "quantcast"
    url: str = "https://feeds.soundcloud.com/users/soundcloud:users:387150302/sounds.rss"
    host_header = "feeds.soundcloud.com"


class AcquiredSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://acquired.libsyn.com/rss."""

    name: str = "acquired"
    url: str = "https://acquired.libsyn.com/rss"
    host_header = "acquired.libsyn.com"


class ToptradersunpluggedSpider(RSSAudioSpider):
    """Spider class for RSS feed: http://www.toptradersunplugged.com/feed/."""

    name: str = "toptradersunplugged"
    url: str = "http://www.toptradersunplugged.com/feed/"
    host_header = "www.toptradersunplugged.com"


class SuperinvestorsSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.soundcloud.com/users/soundcloud:users:5374186/sounds.rss."""

    name: str = "superinvestors"
    url: str = "https://feeds.soundcloud.com/users/soundcloud:users:5374186/sounds.rss"
    host_header = "feeds.soundcloud.com"


class MacrovoicesSpider(RSSAudioSpider):
    """Spider class for RSS feed: http://feeds.macrovoices.com/MacroVoices?format=xml."""

    name: str = "macrovoices"
    url: str = "http://feeds.macrovoices.com/MacroVoices?format=xml"
    host_header = "feeds.macrovoices.com"


class ContrarianSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://contrarian.libsyn.com/rss."""

    name: str = "contrarian"
    url: str = "https://contrarian.libsyn.com/rss"
    host_header = "contrarian.libsyn.com"


class AbsolutereturnSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feed.podbean.com/absolutereturn/feed.xml."""

    name: str = "absolutereturn"
    url: str = "https://feed.podbean.com/absolutereturn/feed.xml"
    host_header = "feed.podbean.com"


class HughhendrySpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.buzzsprout.com/1017043.rss."""

    name: str = "hughhendry"
    url: str = "https://feeds.buzzsprout.com/1017043.rss"
    host_header = "feeds.buzzsprout.com"


class HedgefundtipsSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://anchor.fm/s/12172a20/podcast/rss."""

    name: str = "hedgefundtips"
    url: str = "https://anchor.fm/s/12172a20/podcast/rss"
    host_header = "anchor.fm"


class FocusedcompoundingSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://focusedcompounding.libsyn.com/rss."""

    name: str = "focusedcompounding"
    url: str = "https://focusedcompounding.libsyn.com/rss"
    host_header = "focusedcompounding.libsyn.com"


class ValuewalkSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.soundcloud.com/users/soundcloud:users:325509635/sounds.rss."""

    name: str = "valuewalk"
    url: str = "https://feeds.soundcloud.com/users/soundcloud:users:325509635/sounds.rss"
    host_header = "feeds.soundcloud.com"


class MarketnarrativesSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.transistor.fm/marketnarratives."""

    name: str = "marketnarratives"
    url: str = "https://feeds.transistor.fm/marketnarratives"
    host_header = "feeds.transistor.fm"


class PatrickBoyleSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.buzzsprout.com/1595539.rss."""

    name: str = "patrickboyle"
    url: str = "https://feeds.buzzsprout.com/1595539.rss"
    host_header = "feeds.buzzsprout.com"


class FrednrorySpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.buzzsprout.com/1689226.rss."""

    name: str = "fred_n_rory"
    url: str = "https://feeds.buzzsprout.com/1689226.rss"
    host_header = "feeds.buzzsprout.com"


class TradingrealitySpider(RSSAudioSpider):
    """Spider class for RSS feed: https://claytrader.com/feed/trading-reality."""

    name: str = "tradingreality"
    url: str = "https://claytrader.com/feed/trading-reality"
    host_header = "claytrader.com"


class BettersystemtraderSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://bettersystemtrader.libsyn.com/rss."""

    name: str = "bettersystemtrader"
    url: str = "https://bettersystemtrader.libsyn.com/rss"
    host_header = "bettersystemtrader.libsyn.com"


class ThetwentyminutevcSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://thetwentyminutevc.libsyn.com/rss."""

    name: str = "thetwentyminutevc"
    url: str = "https://thetwentyminutevc.libsyn.com/rss"
    host_header = "thetwentyminutevc.libsyn.com"


class TradeideaspodcastSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://tradeideaspodcast.libsyn.com/rss."""

    name: str = "tradeideaspodcast"
    url: str = "https://tradeideaspodcast.libsyn.com/rss"
    host_header = "tradeideaspodcast.libsyn.com"


class TraidersmidnchatSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://anchor.fm/s/19508ac/podcast/rss."""

    name: str = "traidersmidnchat"
    url: str = "https://anchor.fm/s/19508ac/podcast/rss"
    host_header = "anchor.fm"


class TalkingtradingSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://talkingtrading.com.au/feed/podcast/."""

    name: str = "talkingtrading"
    url: str = "https://talkingtrading.com.au/feed/podcast/"
    host_header = "talkingtrading.com.au"


class TraderslifeSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.buzzsprout.com/1231772.rss."""

    name: str = "traderslife"
    url: str = "https://feeds.buzzsprout.com/1231772.rss"
    host_header = "feeds.buzzsprout.com"


class FastmoneyFeedSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.simplecast.com/szW8tJ16."""

    name: str = "fastmoney_2"
    url: str = "https://feeds.simplecast.com/szW8tJ16"
    host_header = "feeds.simplecast.com"


class StockinvestSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://anchor.fm/s/172f8b38/podcast/rss."""

    name: str = "stockinvest"
    url: str = "https://anchor.fm/s/172f8b38/podcast/rss"
    host_header = "anchor.fm"


class DesiretotradeSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://desiretotrade.libsyn.com/rss."""

    name: str = "desiretotrade"
    url: str = "https://desiretotrade.libsyn.com/rss"
    host_header = "desiretotrade.libsyn.com"


class TradingjusticeSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://tradingjustice.libsyn.com/rss."""

    name: str = "tradingjustice"
    url: str = "https://tradingjustice.libsyn.com/rss"
    host_header = "tradingjustice.libsyn.com"


class TradersimprovedSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feed.podbean.com/tradersimproved/feed.xml."""

    name: str = "tradersimproved"
    url: str = "https://feed.podbean.com/tradersimproved/feed.xml"
    host_header = "feed.podbean.com"


class StocksandjocksSpider(RSSAudioSpider):
    """Spider class for RSS feed: http://stocksandjocks.net/show-archives/feed/snj."""

    name: str = "stocksandjocks"
    url: str = "http://stocksandjocks.net/show-archives/feed/snj"
    host_header = "stocksandjocks.net"


class SwingtradingSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://anchor.fm/s/3433c3d4/podcast/rss."""

    name: str = "swingtrading"
    url: str = "https://anchor.fm/s/3433c3d4/podcast/rss"
    host_header = "anchor.fm"


class IgtradingthemarketsSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.blubrry.com/feeds/igtradingthemarkets.xml."""

    name: str = "igtradingthemarkets"
    url: str = "https://feeds.blubrry.com/feeds/igtradingthemarkets.xml"
    host_header = "feeds.blubrry.com"


class ProfitstrategiesSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://anchor.fm/s/188c356c/podcast/rss."""

    name: str = "profitstrategies"
    url: str = "https://anchor.fm/s/188c356c/podcast/rss"
    host_header = "anchor.fm"


class FuturesradioshowSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://anthonycrudele.com/futuresradioshow/feed/podcast."""

    name: str = "futuresradioshow"
    url: str = "https://anthonycrudele.com/futuresradioshow/feed/podcast"
    host_header = "anthonycrudele.com"


class SmartermarketsSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feed.podbean.com/smartermarkets/feed.xml."""

    name: str = "smartermarkets"
    url: str = "https://feed.podbean.com/smartermarkets/feed.xml"
    host_header = "feed.podbean.com"


class ExchangesSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.megaphone.fm/GLD9218176758."""

    name: str = "exchanges_in_gs"
    url: str = "https://feeds.megaphone.fm/GLD9218176758"
    host_header = "feeds.megaphone.fm"


class CapitalistSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.simplecast.com/xOsRQ_c8."""

    name: str = "capitalist"
    url: str = "https://feeds.simplecast.com/xOsRQ_c8"
    host_header = "feeds.simplecast.com"


class MarketbanterSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://anchor.fm/s/308e19dc/podcast/rss."""

    name: str = "marketbanter"
    url: str = "https://anchor.fm/s/308e19dc/podcast/rss"
    host_header = "anchor.fm"


class InvestorhourSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://investorhour.libsyn.com/rss."""

    name: str = "investorhour"
    url: str = "https://investorhour.libsyn.com/rss"
    host_header = "investorhour.libsyn.com"


class ConveregentSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://anchor.fm/s/4fd91d0/podcast/rss."""

    name: str = "converegent"
    url: str = "https://anchor.fm/s/4fd91d0/podcast/rss"
    host_header = "anchor.fm"


class WSUnpluggedSpider(RSSAudioSpider):
    """Spider class for RSS feed: http://sainvestorradio.chooseyourself.libsynpro.com/rss."""

    name: str = "wsunplugged"
    url: str = "http://sainvestorradio.chooseyourself.libsynpro.com/rss"
    host_header = "sainvestorradio.chooseyourself.libsynpro.com"


class SwapSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.acast.com/public/shows/5f875b6d04b8b24d930fa60f."""

    name: str = "swap"
    url: str = "https://feeds.acast.com/public/shows/5f875b6d04b8b24d930fa60f"
    host_header = "feeds.acast.com"


class ChatwithtradersSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://chatwithtraders.libsyn.com/rss."""

    name: str = "chatwithtraders"
    url: str = "https://chatwithtraders.libsyn.com/rss"
    host_header = "chatwithtraders.libsyn.com"


class DerivativesSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://www.spreaker.com/show/4654164/episodes/feed."""

    name: str = "derivatives"
    url: str = "https://www.spreaker.com/show/4654164/episodes/feed"
    host_header = "www.spreaker.com"


class TheDerivativeSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://anchor.fm/s/11908b3c/podcast/rss."""

    name: str = "the_derivative"
    url: str = "https://anchor.fm/s/11908b3c/podcast/rss"
    host_header = "anchor.fm"


class AlphaexchangeSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.simplecast.com/8g9ryFGf."""

    name: str = "alphaexchange"
    url: str = "https://feeds.simplecast.com/8g9ryFGf"
    host_header = "feeds.simplecast.com"


class TradingnutSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://tradingnut.com/feed/tradingnut/."""

    name: str = "tradingnut"
    url: str = "https://tradingnut.com/feed/tradingnut/"
    host_header = "tradingnut.com"


class MoneytreeinvestingSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://moneytreeinvesting.libsyn.com/rss."""

    name: str = "moneytreeinvesting"
    url: str = "https://moneytreeinvesting.libsyn.com/rss"
    host_header = "moneytreeinvesting.libsyn.com"


class TastytradeSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.tastytrade.com/podcast.rss."""

    name: str = "tastytrade"
    url: str = "https://feeds.tastytrade.com/podcast.rss"
    host_header = "feeds.tastytrade.com"


class WSBreakfastSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.megaphone.fm/SA6208285727."""

    name: str = "wsbreakfast"
    url: str = "https://feeds.megaphone.fm/SA6208285727"
    host_header = "feeds.megaphone.fm"


class RoundtableSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.megaphone.fm/SA7323769782."""

    name: str = "roundtable"
    url: str = "https://feeds.megaphone.fm/SA7323769782"
    host_header = "feeds.megaphone.fm"


class LongviewSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://feeds.simplecast.com/5SEwkJYi."""

    name: str = "longview"
    url: str = "https://feeds.simplecast.com/5SEwkJYi"
    host_header = "feeds.simplecast.com"


class MillenialSpider(RSSAudioSpider):
    """Spider class for RSS feed: https://rss.art19.com/millennial-investing."""

    name: str = "millenial"
    url: str = "https://rss.art19.com/millennial-investing"
    host_header = "rss.art19.com"


class MyWallstSpider(RSSAudioSpider):
    """A spider class for RSS feed: https://feed.podbean.com/mywallst/feed.xml."""

    name: str = "mywallst"
    url: str = "https://feed.podbean.com/mywallst/feed.xml"
    host_header = "feed.podbean.com"
