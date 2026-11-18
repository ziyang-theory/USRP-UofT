# Project option: Extend SecCol

How can two AI agents schedule a meeting when neither user wants to share their calendar? Ziyang Jin’s paper [*SecCol: Agent Collaboration Over Private Data* (PDF)](seccol.pdf) uses this question to introduce a framework for computing on private data.

## How SecCol schedules a meeting

Suppose Alice is free on Monday and Tuesday, and Bob is free on Tuesday and Thursday. Their agents ask for one shared slot. Each user’s policy engine checks whether to allow the request. If both approve, the agents pass references to the calendars to their respective runtimes. The runtimes read the calendars and jointly compute a slot using secure multiparty computation (MPC). Both agents receive Tuesday. Neither needs the other user’s calendar entries to arrange the meeting.

The answer itself reveals that both users are free on Tuesday. What else could an agent learn from several approved requests? This is why SecCol’s policy engine considers the history of requests when deciding whether to allow another one. Section 4 describes the policy, and Section 5 walks through scheduling. The prototype in Section 6 uses an ideal functionality to stand in for MPC, so its reported scheduling time excludes the cost of running a cryptographic protocol between the users.

## Two possible extensions

- **Study what repeated scheduling reveals.** Start with four time slots and let each request specify a public meeting window. Return the earliest common slot in that window, or “none” if there is no overlap. Which of Bob’s possible calendars are consistent with Alice’s availability and the answer? Enumerate them, then repeat after a second request. Compare a policy that limits how often Alice can ask with one that also rejects overlapping windows. On the same sequence of requests, count how many calendars remain possible and how many meetings each policy allows.
- **Run the scheduling task with a concrete MPC protocol.** Encode each calendar as one availability bit per slot and use a two-party MPC library to return the first common slot, or “none,” to both agents. Check the result against a plain implementation on synthetic calendars, including cases with zero or several common slots. Then measure end-to-end time and bytes exchanged as the number of slots grows. State which behavior the chosen protocol tolerates if a participant deviates from it.

For the [Week 6 proposal](../../roadmap.md#week-6), choose one question, identify the closest prior work, and explain what your first example or experiment would tell you.
