---
title: "Execution Costs, Liquidity, and Trade Sequencing"
date: 2026-04-22
note_category: "Microstructure"
tags:
  - Trade execution
  - Transaction costs
  - Futures
  - Spreads
summary: "Some practical thoughts on execution: late fills, liquidity, volatility, and why the order you execute a structure in can matter more than people first think."
---

People often talk about signals, models, and backtests as if execution is the last step. I do not think that is quite right. Execution is part of the strategy. It took me some time to arrive at this realisation.

I think this matters even more when the trade is not just one leg, but some combination of outrights and spreads. On paper, the position can look simple enough. In reality, once the signal is emitted, you still have to decide what to do first, what can wait, and what kind of risk you are carrying while the structure is only partially filled.


## Why execution order matters

When a signal is emitted, the question is not only what to trade, but also what to cover first.

This is not always obvious. A simple place to start is to compare the daily moves of the outright against the daily moves of the spread.

Usually for Brent Futures (I'm tempted to just say always, but I've got to caveat), the outright is the more volatile leg. The bid/ask can be wide, and the size sitting on the best bid and offer can be much smaller than what you see in the spread market. So if the market starts moving, the outright is often the one that gets away from you first.

Spreads are often slower -- they are somewhat 'market' neutral in that sense. That does not mean they are easy, or that they are cheap to trade, only that the immediate execution risk is often more concentrated in the outright.


## The practical implication

If execution is manual, you often would want to cover the necessary outright first, then take your time working the spreads.

The rough logic is:

1. The outright carries more immediate price risk.
2. Its liquidity at the top of book is often thinner in size terms.
3. If you are late on the outright, you can lose the core economics of the trade, or just give away a significant portion of the P&L.
4. Also, there is often some correlation between the outright and the spread, so the sequence can affect how much value you actually manage to preserve.

So even if the trade is really a multi-leg structure, the outright may still be the part that needs attention first, unless you're dealing something like a size of 10x on the outright and 2,000x on the spreads. Basic logical thinking is still required.


## Costs are broader than the bid/ask

When people talk about costs, they usually start with bid/ask, commissions, and fees. That is fair, but it is also incomplete.

There are other costs as well:

1. Slippage from urgency
2. Impact from leaning on thin liquidity
3. Opportunity cost from delayed fills
4. Residual risk while the trade is only partially built

That last point matters quite a bit. If the outright is filled but the spreads are not, or vice versa, then the risk you actually hold is not the one you originally intended to hold. The trade in the book is temporarily different from the trade in your research.

Additionally, points 1 and 2 reminded me of one incident I had some time back. It is not exactly a story about how to estimate transaction costs properly. It is more a reminder that when liquidity gets bad, you also need to think about how to structure your way out of the position.

We had to get into an outright Brent position of around 150 lots as part of a strategy. We entered, but later realised we had gotten into an expiring contract that would cease trading by the end of the day. 150 lots is by no means a large size for Brent, but on the last trading day the market was thin and very choppy.

At that point, the options were fairly limited:

1. Sweep the thin market and keep moving the price against ourselves
2. Sit on limits, maybe iceberg the order, and hope for the best
3. Roll the position through spreads first, then exit through outrights

The first two were not great choices. The market was thin, the timeline was tight, and every minute wasted would likely leave us with even worse liquidity and more price drift risk. We ended up going with the third route and managed to get out with minimal losses.

## Research motivation

This was more or less a random recollection I had recently, so I thought I would write it down. But it also reminded me that I should probably do a proper study on the market microstructure of different asset classes such as precious metals, agriculture, fixed income, and energy.

I did some work on this some time back, and I think it would be worth converting into a more formal research piece to share here. The broad point is simple enough: execution is not just something that comes after the signal. In a lot of cases, execution is part of whether the signal is worth anything in the first place.
