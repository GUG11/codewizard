# Principles of Agent Curation

These principles are how Codewizard is built on

1. **Keep decision authority firmly with users; fully delegate execution to agents.** Users should articulate their intentions as goals or missions, delegate execution to agents, and refrain from intervening in how agents execute. Agents should carry out the missions at their own discretion. Both Claude Code and Codex have plan mode, but this mode focus too much on how while pay inssufficient attention to what. On the contrary, the agent excels at how but lack judgement on what, esepcially when trade-off are needed.

1. **No technically correct but valueless rhetoric. Instruct AI with examples"**. AI doesn't lack good will words like "communicate effectly", "you are a senior software engineer", "verified facts from user/code/logs/docs". AI lack the context and judgement to reason correctly. It doesn't know how to find a good balance between over communnication and under communication", what are the exact behaviors of a senior software engineer under different kinds of situations, what code are really executed online or deprecated, what logs are critical. Instead of telling these vague requirements, you should use example to help AI build the judgement.
