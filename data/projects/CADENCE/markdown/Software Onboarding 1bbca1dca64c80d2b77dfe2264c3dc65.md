# Software Onboarding

I talked with Alex and got some things cleared up through that, as well as the conversation me and Ceir had with the hardware guy. This doc is my best to summarize all of that, and try and get everyone on the same page for writing requirements and understanding our role on the team

### Role of flight/payload software

- Flight software
    - encompasses most of the software on board
    - i like to think of it as the “brain” of the satellite (i.e. the communications team handle the physical hardware of communications, similar to the human body and an arm, but we still need to write the software that controls these communications, interfaces with whatever communication protocol they decide to use, as well as write systems to send, receive, and store data
    - Flight software isn’t just literally software for flight, it is everything that manages the health of the spacecraft, including software in place to manage power, thermals, etc.
    - our goal is to “keep the spacecraft alive”, as well as facilitating things like data storage, communication, etc.
    - we will be communicating pretty heavily with all the other teams, like avionics, power systems, and communications, as the code we write will involve the hardware they are creating
- Payload software
    - I have less of an idea about this one, but I’m pretty sure it’s similar, if not the same as flight software (i think payload software/science is usually included in the flight software
    - the main goal of payload is to handle the science and mission-specific data collection and processing (i.e. the radiation collection in the case of CADENCE)
    - through this team we will be implementing data collection, storage, and transmission
    - like said for flight software, this is the brains of the body → avionics & hardware is working on the **physical** aspect of the satellite (like the dosimeter), but the code to interface with this dosimeter and any other sensors, as well as creating a system that will record and store the data from the sensors is up to payload software
    - similarly, through this we will have to work closely with the other teams, I think mostly avionics/hardware

The following image was shown to me by alex to show the kinds of things included in flight software; It’s a screenshot of the mars ingenuity helicopter and rover interface. From it you can see things such as navigation, power control, comms, etc. 

![image.png](image%20426.png)

This next picture i borrowed (stole) from what Tri posted in the Comms-rf discord channel. It’ll give you a better idea of our two sections and how we connect with others. It doesn’t exactly have everything, but I think it’s a cool visual

![image.png](image%20427.png)

### Writing Requirements

- I don’t think we’re responsible for mission objectives / Tier 1 requirements, just expanding into Tier 2 and Tier 3
- As software, I think our contribution to requirements kinda reach into every category, because like I said we are the ones that will be implementing all the hardware and systems together via code
- Requirement I want you guys to focus on are things that define how the systems and controlled/managed, as well as systems that will be in place that you think we will have to create (like database storage, communication interfaces, etc.)
- I wouldn’t worry about being wrong about writing reqs, I just want you guys to start writing stuff down so we can work through it as a team
- During the meeting we talked about not really understanding what kind of requirements we should write because it feel’s like we’re stepping on the toes of other teams, and that's because our role in software is literally to dive into their sections and help them implement everything
    - Ex) MO-4.0 : The satellite shall collect radiation data at a TBD frequency over the South Atlantic Anomaly and Generate an accumulated radiation dose rate over TBD timesteps
    - A requirement we could write for this is: “The satellite shall have a system in place to store and send radiation data” which could then be broken into tier 3 requirements such as “The system shall store data collecting into a database”
    - these aren’t complete examples but you get the point → “the satellite shall have a system in place to monitor power usage and keep it at a safe level for operations” “the satellite shall have a system that receives instructions from a ground station” “the system shall be able to execute these instructions onboard remotely” stuff like that
    - again we are the brains, the “how” in regard to the mission

---

I’m still not 100% about the software design paper, I’m going to look into it more at another time, and probably go bother alex or kelly again about it, but we do need to start helping with these requirements so I hope all of this helps out ^^