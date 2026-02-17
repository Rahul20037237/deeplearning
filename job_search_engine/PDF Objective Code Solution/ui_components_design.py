# ============================================================================
# USER INTERFACE COMPONENTS - RESPONSIVE DESIGN SYSTEM
# ============================================================================

ui_components = {
    "design_system": {
        "framework": "React + TypeScript",
        "styling": "Tailwind CSS + shadcn/ui components",
        "state_management": "Redux Toolkit + React Query",
        "routing": "React Router v6",
        "forms": "React Hook Form + Zod validation",
        "responsive": "Mobile-first design (320px to 4K)",
        "accessibility": "WCAG 2.1 AA compliant",
        "theme": {
            "colors": {
                "primary": "#1D1D20",  # Zerve dark background
                "text_primary": "#fbfbff",  # Primary text
                "text_secondary": "#909094",  # Secondary text
                "accent": "#ffd400",  # Highlights
                "success": "#17b26a",  # Success states
                "error": "#f04438",  # Error states
                "blue": "#A1C9F4",
                "orange": "#FFB482",
                "green": "#8DE5A1"
            },
            "fonts": {
                "primary": "Inter, system-ui, sans-serif",
                "heading": "Poppins, Inter, sans-serif"
            },
            "breakpoints": {
                "mobile": "320px - 639px",
                "tablet": "640px - 1023px",
                "desktop": "1024px - 1279px",
                "wide": "1280px+"
            }
        }
    },
    
    "navigation_header": {
        "component": "Navbar",
        "features": [
            "Logo with brand name",
            "Search bar (prominent, auto-complete)",
            "Navigation links (Jobs, Companies, Profile, Applications)",
            "User avatar dropdown (Profile, Settings, Logout)",
            "Notification bell with badge",
            "Dark mode toggle",
            "Mobile hamburger menu"
        ],
        "responsive_behavior": {
            "mobile": "Collapsed hamburger menu, search icon only",
            "tablet": "Partial nav links, full search",
            "desktop": "Full navigation with all elements"
        },
        "html_structure": '''
<header className="sticky top-0 z-50 bg-primary border-b border-gray-800">
  <nav className="container mx-auto px-4 py-3 flex items-center justify-between">
    <div className="flex items-center gap-8">
      <Logo />
      <SearchBar className="hidden md:block" />
    </div>
    <div className="hidden lg:flex items-center gap-6">
      <NavLink to="/jobs">Jobs</NavLink>
      <NavLink to="/companies">Companies</NavLink>
      <NavLink to="/applications">Applications</NavLink>
    </div>
    <div className="flex items-center gap-4">
      <NotificationBell />
      <UserMenu />
      <MobileMenuToggle className="lg:hidden" />
    </div>
  </nav>
</header>
        '''
    },
    
    "job_search_interface": {
        "component": "JobSearchPage",
        "layout": "Two-column (filters sidebar + results grid)",
        "features": [
            "Intelligent search bar with auto-complete",
            "Location input with geolocation",
            "Advanced filters (collapsible on mobile)",
            "Job cards with key details",
            "Infinite scroll / pagination",
            "Save job button",
            "Quick apply button",
            "Sorting options (relevance, date, salary)"
        ],
        "filters": {
            "experience_level": ["Fresher", "0-1 years", "1-2 years", "2-3 years"],
            "job_type": ["Full-time", "Part-time", "Internship", "Contract"],
            "location": "City/region with autocomplete",
            "salary_range": "Slider (₹0 - ₹15 LPA)",
            "posted_date": ["Last 24h", "Last 7 days", "Last 30 days"],
            "company_size": ["Startup", "Mid-size", "Enterprise"],
            "skills": "Multi-select tags",
            "remote": "Toggle for remote/hybrid/onsite"
        },
        "job_card_design": '''
<div className="bg-gray-900 border border-gray-800 rounded-lg p-4 hover:border-accent transition">
  <div className="flex items-start justify-between">
    <div className="flex gap-3">
      <img src={companyLogo} className="w-12 h-12 rounded" />
      <div>
        <h3 className="text-lg font-semibold text-text-primary">{jobTitle}</h3>
        <p className="text-sm text-text-secondary">{companyName}</p>
        <div className="flex gap-2 mt-2">
          <Badge>{experienceLevel}</Badge>
          <Badge>{jobType}</Badge>
          <Badge>{location}</Badge>
        </div>
      </div>
    </div>
    <div className="flex gap-2">
      <Button variant="ghost" size="icon"><BookmarkIcon /></Button>
      <Button variant="default">Quick Apply</Button>
    </div>
  </div>
  <div className="mt-3 flex items-center justify-between">
    <div className="flex gap-4 text-sm text-text-secondary">
      <span>💰 {salaryRange}</span>
      <span>📍 {location}</span>
      <span>🕒 {postedDate}</span>
    </div>
    <span className="text-success font-semibold">{matchScore}% match</span>
  </div>
</div>
        ''',
        "responsive_behavior": {
            "mobile": "Filters in bottom sheet modal, single column cards",
            "tablet": "Filters in collapsible sidebar, 2 column grid",
            "desktop": "Persistent filters sidebar, 2-3 column grid"
        }
    },
    
    "job_details_page": {
        "component": "JobDetailsModal",
        "features": [
            "Full job description (parsed and formatted)",
            "Company information card",
            "Skills required (with user match indicators)",
            "Salary and benefits",
            "Application form (inline or modal)",
            "Similar jobs recommendations",
            "Share job button (copy link, social)",
            "Report job button"
        ],
        "layout": '''
<div className="max-w-5xl mx-auto p-6">
  <div className="grid md:grid-cols-3 gap-6">
    {/* Main content - 2 columns */}
    <div className="md:col-span-2 space-y-6">
      <JobHeader />
      <JobDescription />
      <RequiredSkills />
      <CompanyDetails />
      <SimilarJobs />
    </div>
    
    {/* Sidebar - 1 column */}
    <div className="space-y-4">
      <ApplicationCard />
      <JobInfoCard />
      <CompanyCard />
      <ShareButtons />
    </div>
  </div>
</div>
        ''',
        "application_flow": {
            "step_1": "Resume selection (uploaded or create new)",
            "step_2": "Cover letter (optional, AI-assisted)",
            "step_3": "Additional questions from employer",
            "step_4": "Review and submit",
            "validation": "Real-time with React Hook Form + Zod"
        }
    },
    
    "user_profile_page": {
        "component": "ProfilePage",
        "sections": [
            "Profile header (photo, name, headline)",
            "Contact information (editable)",
            "Education (add/edit/delete)",
            "Experience (timeline view)",
            "Skills (tags with endorsements)",
            "Certifications",
            "Resume upload/manage",
            "Portfolio links",
            "Privacy settings"
        ],
        "features": [
            "Inline editing with auto-save",
            "Profile completion percentage",
            "Public profile URL",
            "Export profile as PDF",
            "Skill gap analysis widget"
        ],
        "profile_header_design": '''
<div className="bg-gradient-to-r from-blue to-green rounded-lg p-6 text-center">
  <Avatar size="xl" src={userPhoto} />
  <h1 className="text-2xl font-bold text-text-primary mt-4">{userName}</h1>
  <p className="text-text-secondary">{headline}</p>
  <div className="flex justify-center gap-4 mt-4">
    <Badge>{location}</Badge>
    <Badge>{experienceLevel}</Badge>
  </div>
  <div className="flex justify-center gap-3 mt-4">
    <Button variant="default">Edit Profile</Button>
    <Button variant="outline">View Public Profile</Button>
  </div>
  <ProgressBar value={profileCompletion} label="Profile Completion" />
</div>
        ''',
        "responsive_behavior": {
            "mobile": "Stacked sections, collapsible cards",
            "desktop": "Two-column layout (main content + sidebar)"
        }
    },
    
    "application_management": {
        "component": "ApplicationsPage",
        "features": [
            "Application status pipeline view",
            "Filter by status (applied, reviewing, interview, rejected, accepted)",
            "Sort by date, company, status",
            "Application cards with timeline",
            "Withdraw application button",
            "Notes/reminders for each application",
            "Interview scheduler integration"
        ],
        "status_pipeline": {
            "stages": ["Applied", "Reviewing", "Interview", "Offer", "Rejected", "Accepted"],
            "visualization": "Kanban board or list view toggle"
        },
        "application_card": '''
<div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
  <div className="flex items-center justify-between">
    <div className="flex gap-3">
      <img src={companyLogo} className="w-10 h-10 rounded" />
      <div>
        <h3 className="font-semibold text-text-primary">{jobTitle}</h3>
        <p className="text-sm text-text-secondary">{companyName}</p>
      </div>
    </div>
    <Badge variant={statusColor}>{status}</Badge>
  </div>
  <div className="mt-3 text-sm text-text-secondary">
    <p>Applied on: {applicationDate}</p>
    <p>Last update: {lastUpdate}</p>
  </div>
  <div className="mt-3 flex gap-2">
    <Button variant="ghost" size="sm">View Details</Button>
    <Button variant="ghost" size="sm">Add Note</Button>
    <Button variant="destructive" size="sm">Withdraw</Button>
  </div>
</div>
        ''',
        "responsive_behavior": {
            "mobile": "List view only, swipe actions",
            "desktop": "Kanban board or list view toggle"
        }
    },
    
    "admin_dashboard": {
        "component": "AdminDashboard",
        "access_control": "RBAC - Admin/Moderator roles only",
        "sections": [
            "Analytics overview (KPIs)",
            "User management (search, filter, ban/unban)",
            "Job moderation queue",
            "Reported content review",
            "System health monitoring",
            "Search analytics",
            "Application statistics"
        ],
        "kpi_cards": [
            "Total users (with growth %)",
            "Total jobs posted",
            "Total applications",
            "Active users (last 7 days)",
            "Average match score",
            "Top searched skills",
            "Conversion rate (search → apply)"
        ],
        "moderation_queue": '''
<div className="space-y-4">
  <h2 className="text-xl font-bold">Job Moderation Queue</h2>
  {jobs.map(job => (
    <div key={job.id} className="bg-gray-900 border border-gray-800 rounded-lg p-4">
      <div className="flex justify-between">
        <div>
          <h3 className="font-semibold">{job.title}</h3>
          <p className="text-sm text-text-secondary">{job.company}</p>
          <p className="text-xs mt-2">Reported by: {job.reporter} | Reason: {job.reason}</p>
        </div>
        <div className="flex gap-2">
          <Button variant="success" onClick={() => approve(job.id)}>Approve</Button>
          <Button variant="destructive" onClick={() => reject(job.id)}>Reject</Button>
          <Button variant="outline" onClick={() => viewDetails(job.id)}>Details</Button>
        </div>
      </div>
    </div>
  ))}
</div>
        ''',
        "analytics_charts": [
            "User registration trend (line chart)",
            "Application funnel (conversion chart)",
            "Top companies by applications (bar chart)",
            "Skills demand heatmap",
            "Geographic distribution (map)",
            "Search queries word cloud"
        ]
    },
    
    "form_validations": {
        "library": "React Hook Form + Zod",
        "validation_rules": {
            "email": "Valid email format, unique in system",
            "password": "Min 8 chars, 1 uppercase, 1 number, 1 special char",
            "phone": "10 digits, Indian format",
            "resume": "PDF/DOCX only, max 5MB",
            "skills": "Min 3 skills required",
            "experience": "Valid date ranges, no future dates"
        },
        "error_handling": {
            "inline_errors": "Show below field immediately",
            "toast_notifications": "For API errors",
            "form_level_errors": "Summary at top of form"
        },
        "example_schema": '''
import { z } from 'zod';

const profileSchema = z.object({
  email: z.string().email('Invalid email').min(1, 'Email required'),
  phone: z.string().regex(/^[0-9]{10}$/, 'Invalid phone number'),
  skills: z.array(z.string()).min(3, 'At least 3 skills required'),
  resume: z.instanceof(File)
    .refine(file => file.size <= 5_000_000, 'Max file size is 5MB')
    .refine(file => ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'].includes(file.type), 'Only PDF/DOCX allowed')
});
        '''
    },
    
    "real_time_updates": {
        "technology": "WebSocket (Socket.io) + React Query",
        "features": [
            "New job notifications",
            "Application status updates",
            "Message notifications",
            "Live search results",
            "Admin moderation alerts"
        ],
        "implementation": '''
// React Query for real-time updates
const { data: applications } = useQuery({
  queryKey: ['applications'],
  queryFn: fetchApplications,
  refetchInterval: 30000, // Poll every 30s
});

// WebSocket for instant notifications
useEffect(() => {
  const socket = io(API_URL);
  
  socket.on('application_update', (data) => {
    queryClient.invalidateQueries(['applications']);
    toast.success(`Application status updated: ${data.status}`);
  });
  
  socket.on('new_job_match', (job) => {
    toast.info(`New job match: ${job.title}`);
  });
  
  return () => socket.disconnect();
}, []);
        '''
    },
    
    "ux_enhancements": {
        "loading_states": [
            "Skeleton loaders for content",
            "Shimmer effect for images",
            "Spinner for form submissions",
            "Progress bars for uploads"
        ],
        "animations": [
            "Smooth page transitions (Framer Motion)",
            "Card hover effects",
            "Modal slide-in animations",
            "Toast notifications"
        ],
        "accessibility": [
            "Keyboard navigation (Tab, Enter, Escape)",
            "ARIA labels for screen readers",
            "Focus indicators",
            "Color contrast ratio > 4.5:1",
            "Alt text for images"
        ],
        "performance": [
            "Lazy loading for images and components",
            "Code splitting per route",
            "Debounced search input",
            "Virtualized lists for large data",
            "Optimistic updates for better perceived performance"
        ]
    }
}

# ============================================================================
# PRINT UI COMPONENTS DESIGN
# ============================================================================

print("=" * 80)
print("USER INTERFACE COMPONENTS - RESPONSIVE DESIGN SYSTEM")
print("=" * 80)

print("\n🎨 DESIGN SYSTEM:")
ds = ui_components['design_system']
print(f"  • Framework: {ds['framework']}")
print(f"  • Styling: {ds['styling']}")
print(f"  • State Management: {ds['state_management']}")
print(f"  • Forms: {ds['forms']}")
print(f"  • Responsive: {ds['responsive']}")
print(f"  • Accessibility: {ds['accessibility']}")

print("\n  COLOR PALETTE:")
for color, value in ds['theme']['colors'].items():
    print(f"    - {color}: {value}")

print("\n  BREAKPOINTS:")
for bp, range_val in ds['theme']['breakpoints'].items():
    print(f"    - {bp}: {range_val}")

print("\n\n🧭 NAVIGATION HEADER:")
nav = ui_components['navigation_header']
print(f"  Component: {nav['component']}")
print("\n  Features:")
for feat in nav['features']:
    print(f"    - {feat}")
print("\n  Responsive Behavior:")
for device, behavior in nav['responsive_behavior'].items():
    print(f"    • {device.capitalize()}: {behavior}")

print("\n\n🔍 JOB SEARCH INTERFACE:")
search = ui_components['job_search_interface']
print(f"  Component: {search['component']}")
print(f"  Layout: {search['layout']}")
print("\n  Features:")
for feat in search['features']:
    print(f"    - {feat}")

print("\n  FILTERS:")
for filter_name, options in search['filters'].items():
    if isinstance(options, list):
        print(f"    • {filter_name}: {', '.join(options)}")
    else:
        print(f"    • {filter_name}: {options}")

print("\n  Responsive:")
for device, behavior in search['responsive_behavior'].items():
    print(f"    • {device.capitalize()}: {behavior}")

print("\n\n📄 JOB DETAILS PAGE:")
details = ui_components['job_details_page']
print(f"  Component: {details['component']}")
print("\n  Features:")
for feat in details['features']:
    print(f"    - {feat}")

print("\n  Application Flow:")
for step, desc in details['application_flow'].items():
    print(f"    {step}: {desc}")

print("\n\n👤 USER PROFILE PAGE:")
profile = ui_components['user_profile_page']
print(f"  Component: {profile['component']}")
print("\n  Sections:")
for section in profile['sections']:
    print(f"    - {section}")

print("\n  Features:")
for feat in profile['features']:
    print(f"    - {feat}")

print("\n\n📋 APPLICATION MANAGEMENT:")
apps = ui_components['application_management']
print(f"  Component: {apps['component']}")
print("\n  Features:")
for feat in apps['features']:
    print(f"    - {feat}")

print("\n  Status Pipeline:")
stages = apps['status_pipeline']['stages']
print(f"    Stages: {' → '.join(stages)}")
print(f"    Visualization: {apps['status_pipeline']['visualization']}")

print("\n\n👨‍💼 ADMIN DASHBOARD:")
admin = ui_components['admin_dashboard']
print(f"  Component: {admin['component']}")
print(f"  Access Control: {admin['access_control']}")
print("\n  Sections:")
for section in admin['sections']:
    print(f"    - {section}")

print("\n  KPI Cards:")
for kpi in admin['kpi_cards']:
    print(f"    - {kpi}")

print("\n  Analytics Charts:")
for chart in admin['analytics_charts']:
    print(f"    - {chart}")

print("\n\n✅ FORM VALIDATIONS:")
forms = ui_components['form_validations']
print(f"  Library: {forms['library']}")
print("\n  Validation Rules:")
for field, rule in forms['validation_rules'].items():
    print(f"    • {field}: {rule}")

print("\n  Error Handling:")
for err_type, handling in forms['error_handling'].items():
    print(f"    • {err_type.replace('_', ' ').title()}: {handling}")

print("\n\n⚡ REAL-TIME UPDATES:")
realtime = ui_components['real_time_updates']
print(f"  Technology: {realtime['technology']}")
print("\n  Features:")
for feat in realtime['features']:
    print(f"    - {feat}")

print("\n\n🎭 UX ENHANCEMENTS:")
ux = ui_components['ux_enhancements']
print("\n  Loading States:")
for state in ux['loading_states']:
    print(f"    - {state}")

print("\n  Animations:")
for anim in ux['animations']:
    print(f"    - {anim}")

print("\n  Accessibility:")
for a11y in ux['accessibility']:
    print(f"    - {a11y}")

print("\n  Performance:")
for perf in ux['performance']:
    print(f"    - {perf}")

print("\n\n" + "=" * 80)
print("✅ Complete responsive UI component system")
print("✅ Mobile-first design with breakpoints")
print("✅ Real-time updates with WebSocket")
print("✅ Comprehensive form validation")
print("✅ WCAG 2.1 AA accessible")
print("✅ Admin dashboard with RBAC")
print("=" * 80)
