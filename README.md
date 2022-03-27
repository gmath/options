# Draw option expiry graphs
Call and put options can be bought and sold (long and short). They can be combined in interesting ways. This application is intended to help view the payout at expiry when options are chained together.

`./options.py --help`

This image is the result of shorting (writing) 1 call contract (100 shares) with a strike of 90 trading at 9.35.
`python options.py --chain s1c90@9.35`
Since you are writing the call, your maximum profit is the cost of the trade (9.35). If the price of the stock exceeds 90, your return diminishes until the stock price is 90 + 9.35, at which point you break even. If the stock goes above that value, you are at a net loss.
![options](https://user-images.githubusercontent.com/5093063/160262776-96780133-7a7e-4846-844b-0389e30ddc7f.png)


You can chain multiple options together. For example if you thought the price of a stock was stable (not going up or down) within the expiry window, you could short a call and short a put.
`python options.py --chain s1c90@9.35 s1p90@9.35`
![options2](https://user-images.githubusercontent.com/5093063/160262997-ef3cdc6f-48c2-4c92-8702-3f42b9ff2b44.png)
