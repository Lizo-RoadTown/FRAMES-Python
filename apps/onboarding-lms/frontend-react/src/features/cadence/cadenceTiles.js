import { IoRocketSharp, IoPeopleCircleOutline, IoConstructOutline, IoSchoolSharp, IoDocumentsOutline, IoGitBranchOutline, IoSettingsOutline, IoCalendarOutline } from "react-icons/io5";

const cadenceTiles = [
  {
    key: "launch-readiness",
    title: "Launch Readiness",
    description: "Subsystem go / no-go status board and launch blockers.",
    href: "",
    icon: IoRocketSharp,
  },
  {
    key: "key-contacts",
    title: "Key Contacts",
    description: "Primary coordinators and escalation roles for each subsystem.",
    href: "",
    icon: IoPeopleCircleOutline,
  },
  {
    key: "active-workstreams",
    title: "Active Workstreams",
    description: "Linked task views filtered to in-progress milestones.",
    href: "",
    icon: IoGitBranchOutline,
  },
  {
    key: "engineering-updates",
    title: "Engineering Updates",
    description: "Latest subsystem reports and technical decisions.",
    href: "",
    icon: IoConstructOutline,
  },
  {
    key: "onboarding",
    title: "New Hire HQ",
    description: "Orientation guides and onboarding checklists for new teammates.",
    href: "",
    icon: IoSchoolSharp,
  },
  {
    key: "module-library",
    title: "Module Library",
    description: "Reusable playbooks, SOPs, and knowledge base articles.",
    href: "",
    icon: IoDocumentsOutline,
  },
  {
    key: "operations-calendar",
    title: "Operations Calendar",
    description: "Team events, launch rehearsals, and major cadence checkpoints.",
    href: "",
    icon: IoCalendarOutline,
  },
  {
    key: "systems-support",
    title: "Systems Support",
    description: "Escalation runbooks and tooling quick links.",
    href: "",
    icon: IoSettingsOutline,
  },
];

export default cadenceTiles;
