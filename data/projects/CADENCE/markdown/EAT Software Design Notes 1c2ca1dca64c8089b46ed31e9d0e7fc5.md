# EAT Software Design Notes

# Preface

- Software gets more complicated the more you work on it
- All of these design philosophies are recommendations, not hard rules

High Level “common sense”

- Use version control
- Keep a history of software
- Write unit tests
- Review code
    - Maintain quality, allows people to stay updates
- Plan out your design using standards makes things easy to follow

---

# WORKFLOW

- Important to define your process
    - Peer reviews, code coverage, testing and flow, agile process, CI/CD
        - Peer review should happen after design phase, and after implementation
        - Important to review tests sometimes more than implementation, so you can see if what is being reviewed is important
        - Helps you avoid going line-by-line in every piece of code
        - Sometimes it is important to go line-by-line and ensure everything is working
    - How things will occur
    - How priorities are decided
        - Jira, trello, etc
        - Organize and prioritize what is going to be worked on next
    - How tasking is assigned
    - Continuous integration

## VERSION CONTROL

- Git, Mercurial
- Keep everything version controlled
    - Source code
    - Deployment scripts
    - Startup scripts
    - Utility scripts
- Define a process for merging and branching in your workflow
    - Pick whatever makes sense to you
    - Create a branch for individual development, review before merging changes back into the main branch
    - Flow and process of this is up to the team

## REVIEWS

- Helps catch bugs
- Should be held at the end of each new feature “pull/merge requests”
- Check for logical bugs
- Check for style/documentation
    - If software needs to outlast you, documentation becomes very very important
- Check tests, ensure they are covering the correct things
    - If you make good tests, you have a good indicator of functioning code without going line by line

## TESTING

- Many levels to testing
    - Unit testing
        - Make sure code is doing what you think it does at the lowest level (functions/methods/classes are units)
    - Functional resting
        - Higher level, not testing if the method works but if the FEATURE works
    - System testing/integration testing
        - Integrating with the system, making sure everything works together as expected
- Code coverage goal
    - Automate your unit tests, and generate code coverage reports
    - Determine how much coverage you want to be testing (aim for 90%+ coverage for flight, and 80%+ for ground software)
        - Higher the better, but there are diminishing returns
        - Not trying to hit 100% because its very difficult to write tests that create hardware events, like radiation affecting hardware, so its hard to implement tests in code to predict things like this
        - Using simulators/emulators help you get this coverage
    - COSMOS
        - Open source ground software
        - Highly configurable, can be used to debug messages and basic commanding/viewing of telemetry without having to create an entire custom ground system
    - Get to full path testing ASAP
        - Don’t spend time putting in luxury features, get to MVP immediately

## CONSTRAINTS

- Hardware
    - Memory
        - Using high level languages/structures can be RAM intensive, and will change the way you have to code
    - Processing
        - Processor intensive tasks will not go well with low powered processors
        - Sometimes you will not know until you start testings, which is why you need to get to MVP testing immediately
    - Storage
        - Trying to store lots of data onto a small SSD it wont work (obviously)
    - Architecture

## OPERATING SYSTEM

- RTOS
    - Lightweight, close to bare metal, task based with a scheduler
- Linux
    - Common in embedded low level
- Bare metal (none
- All completely different environments, and will determine how software is written

## CONCEPTS

- Finite state machines
    - Useful in software, especially at bare metal with no OS
    - Used frequently
    - Bare metal has no scheduler, and you’re managing one core, one processor, on thread, that you have to make sure goes around correctly, so making a finite state machine helps you organize your code at low levels
    - Useful in describing mission “modes”
- Agile development, iterative design
    - Create MVP, then go back and iterate after you have a minimum viable product

## ASSURANCE

- Better hardware makes software job easier
- On the software side, you can use things like hashes, MD5 checking for corruption,
- File scrubbing
- TMR (hardware term) creating redundant software (3 copies of 1 file, then vote on which to use)
- Journaling file systems helps with power loss events, corruption, etc.
- ECC(?)

# DESIGN

---

## DESIGN: DIAGRAMS

- Software block diagrams
    - Explains the process flow
    - Show interactions in a visual way
    - One of the hardest things as a software engineer is communication with your team, and planning in this way helps that
    - Make it as detailed as you can
    - Will help seeing what testing needs to be done
- Timing Diagrams

## DESIGN: FSW CORE

- Prefer a distributed design
    - Has more modern design principles of different services with individual domains, and allow software to function in a deteriorated state
    - Design difference applications (managers) to control individual hardware pieces
        - I.e radio manager
    - Core applications like handling commands and sending telemetry, or interacting with OS, file management, etc.
        - Core can be used across missions, so these should be robust
- Monolithic may be easier, but is harder to manually intervene when complications arise
- Microcontrollers
    - Mimic separate applications by servicing separate routines in a state machine
- Design depends on library
    - NASA cFS - CFE is main core
    - kubOS - separate applications with core features

## DESIGN: COMMON CODE

- You want your code/modules/plugins to be generic, reusable that can be potentially used in future missions, or between your flight and ground software
- Some software will be mission specific, planning will help determine this
- BufferUtils
    - Serialization code will get reused almost everywhere
    - Bufferutils means writing common utilities for manipulating buffers or serialized bytes
    - Common keepalive and watchdog handling
        - Keeping al library will help so they dont need to be rewritten every time
- Utilize configuration files
    - Common style; xml, json, environment files, command line arguments
    - Strategy depends on how you want to make changes on orbit
        - Using config files, you have to think about how to change things while in orbit
        - Command line arguments have the same idea
        - Maybe you have commands that you send up to write to the config files
- Shared memory
    - Timing, and reboot count
    - Can be used to synch timing when handling gps signals

## DESIGN: MESSAGING

- Internal communication between applications or other hardware running flight software
- Messaging can happen at all levels (ground to radio, relay between, etc)
- C&DH
    - If you have a distributed architecture, there is typically a command processor that does the routing
    - Dont have to do this, just one way to approach
- Protocols
    - Use standards when you can: Space packets
    - Another case where libraries you pick may drive you to other implementation
    - Sometimes there is native support
- Using UDP or TCP
    - Trade whether or not you need TCP
    - UDP may be enough, but you have to understand packets may come in out of order, and some may be dropped completely
    - TCP guarantees order and delivery
    - Understand protocols, understand tradeoffs, understand requirements of connections
    - e.g) a lot of commands have scheduled execution time; it doesn’t matter when it gets there because you will look at the time and order it anyways

## Design: Faults

- Basic concept- detect a condition and respond
- Responses:
    - Hard & soft resets
    - Change mode
        - Puts you in a known, good state
    - Restart application
        - If you have a distributed system, just restart one
    - Log and error
        - Hope operators can get to it and fix it (hopefully not a critical error)
    - Other
- Common Faults:
    - Last successful uplink
        - Have a timer that times out after 3 days after not receiving commands, then identifies this as a fault. System tries to reconnect and make sure everything is connected and running appropriately
    - Time since comms with subsystem
        - If gps hasn’t output data in 30 seconds, its time to reset it
    - Low battery
        - Reduce power draw
    - ADCS momentum too high
        - Faults that will handle and switch to a safe mode
    - Watchdogs
        - Try to watchdog everything
        - Watchdogs watching watchdogs
        - Idea is that they are pinging a watchdog, like toggling a pin or sending a message, and if the pings don’t happen for a while that system has to be reset/restarted

## DESIGN: MODES

- Want your modes to be well tested and well designed
- Switching into a mode puts you in a known state for certain operations
    - Safe mode - extremely well testing, guaranteed to be a good state, always have one to go back to
- Things to define
    - Telemetry gathering
    - Subsystem power states
    - The faults being monitored during this mode
        - If hardware isn’t used for a certain mode, you don’t want to monitor it

## OTHER TIPS

- Log levels and verbose logging
    - You will be mad at yourself for not logging in the future
    - Put in time to log everything or else you will regret it
- Keep central repo of documents of information
    - Like a wikipedia of all of your collective knowledge