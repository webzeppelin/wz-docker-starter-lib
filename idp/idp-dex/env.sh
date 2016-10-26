# dex worker
export DEX_WORKER_NO_DB=true
export DEX_WORKER_LISTEN="http://0.0.0.0:5556"
export DEX_WORKER_ISSUER="https://idp.wzstarter.org/dex"
# export DEX_WORKER_TLS_CERT_FILE=
# export DEX_WORKER_TLS_KEY_FILE=
export DEX_WORKER_HTML_ASSETS=/opt/dex/static/html
export DEX_WORKER_EMAIL_TEMPLATES=/opt/dex/static/email
export DEX_WORKER_EMAIL_CFG=/opt/dex/static/fixtures/emailer.json
export DEX_WORKER_ENABLE_REGISTRATION=true
export DEX_WORKER_ENABLE_AUTOMATIC_REGISTRATION=false
export DEX_WORKER_ENABLE_CLIENT_REGISTRATION=false
export DEX_WORKER_KEY_SECRETS=oC94U3/eV3ffav7CCtuH4hdMkckmdj0BfVGUjImcDUk=
export DEX_WORKER_OAUTH_CLIENT_ID=IDP_WZSTARTER_ORG
export DEX_WORKER_OAUTH_CLIENT_SECRET=oC94U3/eV3ffav7CCtuH4hdMkckmdj0BfVGUjImcDUk=
# export DEX_WORKER_DB_URL="postgres://coreos:coreos@localhost:5432/dex?sslmode=disable"
export DEX_WORKER_LOG_DEBUG=1
export DEX_WORKER_CONNECTORS=/opt/dex/static/fixtures/connectors.json
export DEX_WORKER_CLIENTS=/opt/dex/static/fixtures/clients.json
export DEX_WORKER_USERS=/opt/dex/static/fixtures/users.json


# dex overlord
export DEX_OVERLORD_KEY_SECRET=oC94U3/eV3ffav7CCtuH4hdMkckmdj0BfVGUjImcDUk=
# export DEX_OVERLORD_DB_URL="postgres://coreos:coreos@localhost:5432/dex?sslmode=disable"
# export DEX_OVERLORD_ADMIN_API_SECRET=gNDbiaFbTOH7dFak9T4QBPwL/sH6bGWljlRfzmGbmsTtNToDdUKkE52pnYqCfS8b9BQk3LbV6OfCN73PmC6veKwrBO2YnZnkwyMp24JNNfqcnkELMLodan+KXYe2kXlGg/APoHjipXOqWcWraYy9DbGzudVOGqlm1pTZexcIpvA=
export DEX_OVERLORD_KEY_PERIOD=1h
