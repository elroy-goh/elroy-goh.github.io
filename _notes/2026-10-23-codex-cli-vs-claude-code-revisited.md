---
title: "Codex CLI vs Claude Code, Revisited"
date: 2026-10-23
note_category: "Tooling"
tags:
  - Codex CLI
  - Claude Code
  - Developer workflow
summary: "A few months on, both are super token hungry. Codex still gives me more quota, but Claude often gets more done. I still enjoy using both though."
---

It has been a few months since I [last wrote about Codex and Claude]({{ '/notes/2026-04-10-codex-cli-vs-claude-cli/' | relative_url }}), and quite a lot has changed since then. I am still using both, but some of the differences have become more obvious with daily use.

Codex has Astra, Claude has Fable. Both are super token hungry. Now OpenAI has [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol), which generally works well, but in my experience it is still a far cry from Claude's [Opus 5.5](https://www.anthropic.com/claude-opus-5-5).

OpenAI definitely provides a huge amount of quota compared to Anthropic. On the plans I use, I can do quite a bit more on Codex before hitting the limit. This was something I liked about it in my previous note, and it is still the case now.

However, with the amount of time Codex spends thinking and constantly checking on long-running tasks, it feels very inefficient with that quota. It runs a script, checks whether it is done, then prints out another progress report saying it is still running. After a while, these updates just feel pointless. I already know the task is running.

Claude, on the other hand, does this much less in my sessions. It thinks, runs a script, and lets it run. It does not seem to need to keep checking just to tell me that nothing has changed. This is something I appreciate, especially for tasks that take a while to complete.

Additionally, GPT-6.1 Sol at medium reasoning effort is nowhere near Opus 5.5 at medium for the work I give them. Even at extra high, Sol sometimes goes into unnecessary loops, thinking about how things should be done and revisiting decisions it has already made. It spends more time and usage, but the final work does not always get any better.

Of course, I want it to think and check its work. But there are times when it feels like it is spending too much effort going back and forth over the same thing. I do not have exact token measurements for all of this, but it is frustrating to watch the usage go up without much progress being made.

All in all, despite the higher quota available on Codex, Claude often gives me a better return in terms of work done and quality of work. Claude's limits are still annoying, but I often feel that I get more out of the usage I do have. These are just my observations from using both for my own work, so your experience may differ.

Codex is super good at image generation though. I have really enjoyed using it for that, and it is one of the reasons I still like having both around. For implementation, I tend to prefer Claude at the moment. But I still enjoy using both, depending on what I am trying to do.
