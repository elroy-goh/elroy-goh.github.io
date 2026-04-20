---
title: "Liquidity Structure Across ICE Brent, CME WTI, and ICE Low Sulphur Gasoil"
date: 2026-04-10
published: false
note_category: "Market Structure"
tags:
  - ICE Brent
  - CME WTI
  - ICE low sulphur gasoil
  - Liquidity
  - Execution
summary: "Why energy futures often trade as a genuinely multi-tenor market, and why that matters for execution, spread selection, and liquidity interpretation."
---

## Thesis

ICE Brent, CME WTI, and ICE low sulphur gasoil do not behave like many futures markets where real liquidity is concentrated almost entirely in one active contract until the roll approaches. In energy, liquidity is often distributed more broadly across the curve, and that changes how I think about execution, spread selection, and where a position should actually be expressed.

The important point is not simply that front-month contracts are active. It is that nearby deferred tenors and calendar spreads can also carry enough liquidity to matter in practice. That creates more flexibility than many people expect if they have spent most of their time in markets where participation is overwhelmingly front-contract driven.

## Observed Market Structure

In ICE Brent, CME WTI, and ICE low sulphur gasoil, liquidity is usually visible in both outrights and spreads rather than in a single outright contract alone. That matters because the cost of expressing a view is not only about top-line volume. It is also about where the curve is genuinely tradable without creating unnecessary impact.

This is especially relevant in energy because:

- outright liquidity can remain meaningful beyond the front contract,
- calendar spreads are often central rather than peripheral to how the market trades,
- displayed spread width does not always tell the full story about executable size,
- and intraday trading quality can vary materially across products and time zones.

That combination makes energy futures feel structurally different from markets where liquidity effectively migrates from one benchmark contract to the next in a much narrower pattern.

## Execution Implications

If liquidity exists across multiple nearby points on the curve, the execution problem becomes more interesting than simply trading the most active contract. The better question is where the trade can be placed with the least friction once spread cost, depth, timing, and desired exposure are considered together.

In practice, that means looking at:

- whether an outright or a spread is the cleaner way to implement the view,
- whether a narrower quoted spread is hiding thinner real size,
- whether the market is active because of fundamental flow or just concentrated around a short intraday window,
- and whether the roll period changes where the true liquidity sits.

That is why I think of liquidity in these products as a curve problem rather than just a front-contract problem.

## Evidence To Add

**Chart placeholder: average daily volume by tenor for ICE Brent, CME WTI, and ICE low sulphur gasoil**

This should show how far meaningful volume extends beyond the front contract for each product.

**Chart placeholder: average quoted bid/ask spread by tenor for ICE Brent, CME WTI, and ICE low sulphur gasoil**

This should compare how quoted spread cost changes as liquidity moves further along the curve.

**Chart placeholder: intraday traded volume by hour for ICE Brent, CME WTI, and ICE low sulphur gasoil**

This should identify when each product is genuinely active rather than merely quoted.

**Chart placeholder: liquidity migration around roll periods for ICE Brent, CME WTI, and ICE low sulphur gasoil**

This should show when depth and activity move from one part of the curve to another.

## Caveats

This note is intentionally qualitative in its current form. The tenor-level claims should be tightened only once the supporting charts are in place. I also expect the answer to vary by product, session, and market regime, so the eventual evidence needs to show distribution and timing rather than a single aggregate statistic.
