# watch the following markets
# ["PaymiumEUR", "Bitcoin24EUR", "BtceUSD", "BitstampUSD", "KrakenEUR",
#  "KrakenUSD", "CampBXUSD", "BitfinexUSD"]

markets = ["PaymiumEUR", "Bitcoin24EUR", "BtceUSD", "BitstampUSD", "KrakenEUR",
           "KrakenUSD", "CampBXUSD", "BitfinexUSD"]
# observers if any
# ["Logger", "DetailedLogger", "TraderBot", "TraderBotSim", "HistoryDumper", "Emailer"]
observers = ["Logger"]

market_expiration_time = 120  # in seconds: 2 minutes

refresh_rate = 20

#### Trader Bot Config
# Access to Private APIs

paymium_username = "PM-U25491455"
paymium_password = "w0h0h0"
paymium_address = "FIXME"  # to deposit btc from markets / wallets

bitstamp_username = "154001"
bitstamp_password = "W0h0h0h0"

# SafeGuards
max_tx_volume = 10  # in BTC
min_tx_volume = 1  # in BTC
balance_margin = 0.05  # 5%
profit_thresh = 1  # in EUR
perc_thresh = 2  # in %

#### Emailer Observer Config
smtp_host = 'FIXME'
smtp_login = 'FIXME'
smtp_passwd = 'FIXME'
smtp_from = 'FIXME'
smtp_to = 'FIXME'

#### XMPP Observer
xmpp_jid = "FROM@jabber.org"
xmpp_password = "FIXME"
xmpp_to = "TO@jabber.org"
