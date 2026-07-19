import { z } from "zod";

export type FieldKind = "text" | "textarea" | "richtext" | "number" | "boolean" | "select" | "list" | "json" | "media";

export type CmsField = {
  name: string;
  label: string;
  kind: FieldKind;
  required?: boolean;
  options?: string[];
  folder?: "images" | "videos" | "documents";
  crop?: boolean;
  table?: boolean;
  filter?: boolean;
};

export type CmsModuleConfig = {
  module: string;
  title: string;
  endpoint: string;
  listEndpoint?: string;
  createEndpoint?: (values: Record<string, unknown>) => string;
  updateEndpoint?: (id: string, values: Record<string, unknown>) => string;
  detailEndpoint?: (id: string) => string;
  deleteEndpoint?: (id: string) => string;
  createMethod?: "POST" | "PUT";
  fields: CmsField[];
  searchFields: string[];
  statusField?: string;
  statusLabels?: [string, string];
  defaultSort: string;
  tableColumns: string[];
};

const commonStatus = { statusField: "is_active", statusLabels: ["Inactive", "Active"] as [string, string] };

export const cmsModules: Record<string, CmsModuleConfig> = {
  hero: {
    module: "hero", title: "Hero", endpoint: "/hero", defaultSort: "created_at", tableColumns: ["heading", "subheading", "is_active"], searchFields: ["heading"], ...commonStatus,
    fields: [
      { name: "heading", label: "Heading", kind: "text", required: true, table: true },
      { name: "subheading", label: "Subheading", kind: "text", table: true },
      { name: "description", label: "Description", kind: "richtext" },
      { name: "button_text", label: "Button Text", kind: "text" },
      { name: "button_link", label: "Button Link", kind: "text" },
      { name: "hero_image_url", label: "Hero Image", kind: "media", folder: "images", crop: true },
      { name: "background_image_url", label: "Background Image", kind: "media", folder: "images", crop: true },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  content: {
    module: "content", title: "Content", endpoint: "/content/content", updateEndpoint: (id) => `/content/${id}`, deleteEndpoint: (id) => `/content/${id}`, detailEndpoint: (id) => `/content/content/${id}`, defaultSort: "display_order", tableColumns: ["title", "slug", "is_active"], searchFields: ["title", "slug"], ...commonStatus,
    fields: [
      { name: "title", label: "Title", kind: "text", required: true, table: true },
      { name: "slug", label: "Slug", kind: "text", table: true },
      { name: "content", label: "Content", kind: "richtext" },
      { name: "fields", label: "Structured Fields", kind: "json" },
      { name: "media_urls", label: "Media URLs", kind: "list" },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  "course-categories": {
    module: "course-categories", title: "Course Categories", endpoint: "/course-categories", defaultSort: "display_order", tableColumns: ["name", "slug", "is_active"], searchFields: ["name", "slug"], ...commonStatus,
    fields: [
      { name: "name", label: "Name", kind: "text", required: true, table: true },
      { name: "slug", label: "Slug", kind: "text", required: true, table: true },
      { name: "description", label: "Description", kind: "richtext" },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  courses: {
    module: "courses", title: "Courses", endpoint: "/courses", defaultSort: "display_order", tableColumns: ["title", "duration", "is_published", "is_active"], searchFields: ["title", "slug"], ...commonStatus,
    fields: [
      { name: "title", label: "Title", kind: "text", required: true, table: true },
      { name: "slug", label: "Slug", kind: "text" },
      { name: "short_description", label: "Short Description", kind: "textarea" },
      { name: "description", label: "Description", kind: "richtext" },
      { name: "thumbnail_url", label: "Thumbnail", kind: "media", folder: "images", crop: true },
      { name: "duration", label: "Duration", kind: "text", table: true },
      { name: "prerequisites", label: "Prerequisites", kind: "list" },
      { name: "tools", label: "Tools", kind: "list" },
      { name: "projects", label: "Projects", kind: "list" },
      { name: "certification", label: "Certification", kind: "text" },
      { name: "registration_url", label: "Registration URL", kind: "text" },
      { name: "is_coming_soon", label: "Coming Soon", kind: "boolean", filter: true },
      { name: "is_published", label: "Published", kind: "boolean", table: true, filter: true },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
      { name: "display_order", label: "Display Order", kind: "number" },
    ],
  },
  teachers: {
    module: "teachers", title: "Teachers", endpoint: "/teachers", defaultSort: "display_order", tableColumns: ["name", "designation", "email", "is_active"], searchFields: ["name", "designation"], ...commonStatus,
    fields: [
      { name: "name", label: "Name", kind: "text", required: true, table: true },
      { name: "designation", label: "Designation", kind: "text", required: true, table: true },
      { name: "biography", label: "Biography", kind: "richtext" },
      { name: "qualification", label: "Qualification", kind: "text" },
      { name: "experience", label: "Experience", kind: "text" },
      { name: "image_url", label: "Photo", kind: "media", folder: "images", crop: true },
      { name: "email", label: "Email", kind: "text", table: true },
      { name: "linkedin_url", label: "LinkedIn URL", kind: "text" },
      { name: "github_url", label: "GitHub URL", kind: "text" },
      { name: "skills", label: "Skills", kind: "list" },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  founders: {
    module: "founders", title: "Founder / Co-Founder", endpoint: "/founders", updateEndpoint: (id) => `/founders/id/${id}`, createEndpoint: (values) => `/founders/${String(values.founder_type || "founder")}`, createMethod: "PUT", defaultSort: "display_order", tableColumns: ["name", "founder_type", "is_active"], searchFields: ["name"], ...commonStatus,
    fields: [
      { name: "founder_type", label: "Founder Type", kind: "select", required: true, options: ["founder", "co_founder"], table: true, filter: true },
      { name: "name", label: "Name", kind: "text", required: true, table: true },
      { name: "bio", label: "Bio", kind: "richtext" },
      { name: "photo_url", label: "Photo", kind: "media", folder: "images", crop: true },
      { name: "education", label: "Education", kind: "json" },
      { name: "experience", label: "Experience", kind: "json" },
      { name: "research", label: "Research", kind: "json" },
      { name: "achievements", label: "Achievements", kind: "json" },
      { name: "social_links", label: "Social Links", kind: "json" },
      { name: "resume_url", label: "Resume", kind: "media", folder: "documents" },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  partners: {
    module: "partners", title: "Partners", endpoint: "/partners", defaultSort: "display_order", tableColumns: ["name", "partner_type", "is_active"], searchFields: ["name"], ...commonStatus,
    fields: [
      { name: "name", label: "Name", kind: "text", required: true, table: true },
      { name: "partner_type", label: "Partner Type", kind: "select", options: ["industry", "college", "technology", "community"], table: true, filter: true },
      { name: "website_url", label: "Website URL", kind: "text" },
      { name: "logo_url", label: "Logo", kind: "media", folder: "images", crop: true },
      { name: "description", label: "Description", kind: "richtext" },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  gallery: {
    module: "gallery", title: "Gallery", endpoint: "/gallery", defaultSort: "display_order", tableColumns: ["alt_text", "category_id", "is_active"], searchFields: ["alt_text", "caption"], ...commonStatus,
    fields: [
      { name: "category_id", label: "Category ID", kind: "number", required: true, table: true, filter: true },
      { name: "image_url", label: "Image", kind: "media", folder: "images", crop: true },
      { name: "alt_text", label: "Alt Text", kind: "text", required: true, table: true },
      { name: "caption", label: "Caption", kind: "richtext" },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  videos: {
    module: "videos", title: "Videos", endpoint: "/videos", defaultSort: "display_order", tableColumns: ["title", "category", "is_featured", "is_active"], searchFields: ["title", "category"], ...commonStatus,
    fields: [
      { name: "title", label: "Title", kind: "text", required: true, table: true },
      { name: "description", label: "Description", kind: "richtext" },
      { name: "category", label: "Category", kind: "text", required: true, table: true, filter: true },
      { name: "youtube_url", label: "YouTube URL", kind: "text" },
      { name: "video_url", label: "Uploaded Video", kind: "media", folder: "videos" },
      { name: "thumbnail_url", label: "Thumbnail", kind: "media", folder: "images", crop: true },
      { name: "duration_seconds", label: "Duration Seconds", kind: "number" },
      { name: "is_featured", label: "Featured", kind: "boolean", table: true, filter: true },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  projects: {
    module: "projects", title: "Projects", endpoint: "/projects", defaultSort: "display_order", tableColumns: ["title", "status", "is_featured", "is_active"], searchFields: ["title"], ...commonStatus,
    fields: [
      { name: "title", label: "Title", kind: "text", required: true, table: true },
      { name: "description", label: "Description", kind: "richtext" },
      { name: "image_url", label: "Image", kind: "media", folder: "images", crop: true },
      { name: "github_url", label: "GitHub URL", kind: "text" },
      { name: "demo_url", label: "Demo URL", kind: "text" },
      { name: "technologies", label: "Technologies", kind: "list" },
      { name: "tags", label: "Tags", kind: "list" },
      { name: "screenshot_urls", label: "Screenshots", kind: "list" },
      { name: "status", label: "Status", kind: "select", options: ["completed", "ongoing", "archived"], table: true, filter: true },
      { name: "is_featured", label: "Featured", kind: "boolean", table: true, filter: true },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  achievements: {
    module: "achievements", title: "Achievements", endpoint: "/achievements", defaultSort: "display_order", tableColumns: ["title", "achievement_type", "is_featured", "is_active"], searchFields: ["title"], ...commonStatus,
    fields: [
      { name: "title", label: "Title", kind: "text", required: true, table: true },
      { name: "description", label: "Description", kind: "richtext" },
      { name: "image_url", label: "Image", kind: "media", folder: "images", crop: true },
      { name: "achievement_type", label: "Achievement Type", kind: "text", table: true, filter: true },
      { name: "is_featured", label: "Featured", kind: "boolean", table: true, filter: true },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  testimonials: {
    module: "testimonials", title: "Testimonials", endpoint: "/testimonials", defaultSort: "display_order", tableColumns: ["student_name", "rating", "is_featured", "is_active"], searchFields: ["student_name", "college"], ...commonStatus,
    fields: [
      { name: "student_name", label: "Student Name", kind: "text", required: true, table: true },
      { name: "college", label: "College", kind: "text" },
      { name: "designation", label: "Designation", kind: "text" },
      { name: "course_completed", label: "Course Completed", kind: "text" },
      { name: "review", label: "Review", kind: "richtext", required: true },
      { name: "rating", label: "Rating", kind: "number", table: true },
      { name: "photo_url", label: "Photo", kind: "media", folder: "images", crop: true },
      { name: "placement_company", label: "Placement Company", kind: "text" },
      { name: "package", label: "Package", kind: "text" },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_featured", label: "Featured", kind: "boolean", table: true, filter: true },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  "success-stories": {
    module: "success-stories", title: "Success Stories", endpoint: "/success-stories", defaultSort: "display_order", tableColumns: ["name", "course", "placement", "is_active"], searchFields: ["name", "course"], ...commonStatus,
    fields: [
      { name: "name", label: "Name", kind: "text", required: true, table: true },
      { name: "image_url", label: "Image", kind: "media", folder: "images", crop: true },
      { name: "course", label: "Course", kind: "text", table: true, filter: true },
      { name: "batch", label: "Batch", kind: "text" },
      { name: "internship", label: "Internship", kind: "text" },
      { name: "placement", label: "Placement", kind: "text", table: true },
      { name: "company_logo_url", label: "Company Logo", kind: "media", folder: "images", crop: true },
      { name: "job_role", label: "Job Role", kind: "text" },
      { name: "college", label: "College", kind: "text" },
      { name: "graduation_year", label: "Graduation Year", kind: "number" },
      { name: "before_journey", label: "Before Journey", kind: "richtext" },
      { name: "after_journey", label: "After Journey", kind: "richtext" },
      { name: "linkedin_url", label: "LinkedIn URL", kind: "text" },
      { name: "achievement_tags", label: "Achievement Tags", kind: "list" },
      { name: "salary", label: "Salary", kind: "text" },
      { name: "story", label: "Story", kind: "richtext", required: true },
      { name: "is_featured", label: "Featured", kind: "boolean", filter: true },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  internships: {
    module: "internships", title: "Internships", endpoint: "/internships", defaultSort: "display_order", tableColumns: ["title", "company", "internship_type", "is_active"], searchFields: ["title", "company"], ...commonStatus,
    fields: [
      { name: "title", label: "Title", kind: "text", required: true, table: true },
      { name: "description", label: "Description", kind: "richtext" },
      { name: "company", label: "Company", kind: "text", table: true },
      { name: "company_logo_url", label: "Company Logo", kind: "media", folder: "images", crop: true },
      { name: "internship_type", label: "Internship Type", kind: "select", options: ["online", "offline", "hybrid"], table: true, filter: true },
      { name: "duration", label: "Duration", kind: "text" },
      { name: "stipend", label: "Stipend", kind: "text" },
      { name: "location", label: "Location", kind: "text" },
      { name: "eligibility", label: "Eligibility", kind: "richtext" },
      { name: "application_url", label: "Application URL", kind: "text" },
      { name: "last_date", label: "Last Date", kind: "text" },
      { name: "skills", label: "Skills", kind: "list" },
      { name: "is_coming_soon", label: "Coming Soon", kind: "boolean", filter: true },
      { name: "is_featured", label: "Featured", kind: "boolean", filter: true },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  events: {
    module: "events", title: "Events", endpoint: "/events", defaultSort: "display_order", tableColumns: ["title", "event_type", "mode", "is_active"], searchFields: ["title"], ...commonStatus,
    fields: [
      { name: "title", label: "Title", kind: "text", required: true, table: true },
      { name: "description", label: "Description", kind: "richtext" },
      { name: "event_type", label: "Event Type", kind: "text", table: true, filter: true },
      { name: "start_date", label: "Start Date", kind: "text" },
      { name: "end_date", label: "End Date", kind: "text" },
      { name: "registration_deadline", label: "Registration Deadline", kind: "text" },
      { name: "event_date", label: "Event Date", kind: "text" },
      { name: "location", label: "Location", kind: "text" },
      { name: "google_maps_url", label: "Google Maps URL", kind: "text" },
      { name: "mode", label: "Mode", kind: "select", options: ["online", "offline", "hybrid"], table: true, filter: true },
      { name: "registration_url", label: "Registration URL", kind: "text" },
      { name: "banner_url", label: "Banner", kind: "media", folder: "images", crop: true },
      { name: "gallery_urls", label: "Gallery URLs", kind: "list" },
      { name: "speaker_details", label: "Speaker Details", kind: "json" },
      { name: "maximum_participants", label: "Maximum Participants", kind: "number" },
      { name: "is_featured", label: "Featured", kind: "boolean", filter: true },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  contact: {
    module: "contact", title: "Contact Requests", endpoint: "/contact", defaultSort: "created_at", tableColumns: ["name", "contact_type", "status", "is_read"], searchFields: ["name", "email", "subject"], statusField: "status", statusLabels: ["new", "read"],
    fields: [
      { name: "contact_type", label: "Contact Type", kind: "select", options: ["student", "college", "industry"], table: true, filter: true },
      { name: "name", label: "Name", kind: "text", required: true, table: true },
      { name: "email", label: "Email", kind: "text", required: true },
      { name: "phone", label: "Phone", kind: "text" },
      { name: "organization", label: "Organization", kind: "text" },
      { name: "designation", label: "Designation", kind: "text" },
      { name: "website", label: "Website", kind: "text" },
      { name: "course_interested", label: "Course Interested", kind: "text" },
      { name: "training_requirements", label: "Training Requirements", kind: "richtext" },
      { name: "expected_students", label: "Expected Students", kind: "number" },
      { name: "preferred_dates", label: "Preferred Dates", kind: "text" },
      { name: "subject", label: "Subject", kind: "text", required: true },
      { name: "message", label: "Message", kind: "richtext", required: true },
      { name: "status", label: "Status", kind: "select", options: ["new", "read", "replied", "archived"], table: true, filter: true },
      { name: "is_read", label: "Read", kind: "boolean", table: true, filter: true },
    ],
  },
  faqs: {
    module: "faqs", title: "FAQ", endpoint: "/faqs", defaultSort: "display_order", tableColumns: ["question", "page", "category", "is_active"], searchFields: ["question"], ...commonStatus,
    fields: [
      { name: "question", label: "Question", kind: "text", required: true, table: true },
      { name: "answer", label: "Answer", kind: "richtext", required: true },
      { name: "page", label: "Page", kind: "text", table: true, filter: true },
      { name: "category", label: "Category", kind: "select", options: ["admissions", "courses", "internships", "placements", "payments", "general"], table: true, filter: true },
      { name: "seo_slug", label: "SEO Slug", kind: "text", required: true },
      { name: "is_featured", label: "Featured", kind: "boolean", filter: true },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  settings: {
    module: "settings", title: "Website Settings", endpoint: "/settings", listEndpoint: "/settings/all", defaultSort: "updated_at", tableColumns: ["site_name", "default_language", "maintenance_mode"], searchFields: ["site_name"], statusField: "maintenance_mode", statusLabels: ["Live", "Maintenance"],
    fields: [
      { name: "site_name", label: "Site Name", kind: "text", required: true, table: true },
      { name: "tagline", label: "Tagline", kind: "text" },
      { name: "default_language", label: "Default Language", kind: "text", table: true },
      { name: "timezone", label: "Timezone", kind: "text" },
      { name: "site_logo_url", label: "Site Logo", kind: "media", folder: "images", crop: true },
      { name: "favicon_url", label: "Favicon", kind: "media", folder: "images", crop: true },
      { name: "hero_defaults", label: "Hero Defaults", kind: "json" },
      { name: "contact_information", label: "Contact Information", kind: "json" },
      { name: "social_links", label: "Social Links", kind: "json" },
      { name: "email_settings", label: "Email Settings", kind: "json" },
      { name: "theme_settings", label: "Theme Settings", kind: "json" },
      { name: "homepage_configuration", label: "Homepage Configuration", kind: "json" },
      { name: "analytics_keys", label: "Analytics Keys", kind: "json" },
      { name: "seo_defaults", label: "SEO Defaults", kind: "json" },
      { name: "maintenance_mode", label: "Maintenance Mode", kind: "boolean", table: true, filter: true },
      { name: "maintenance_message", label: "Maintenance Message", kind: "richtext" },
      { name: "default_theme", label: "Default Theme", kind: "select", options: ["light"] },
      { name: "pagination_size", label: "Pagination Size", kind: "number" },
    ],
  },
  navigation: {
    module: "navigation", title: "Navigation", endpoint: "/navigation", defaultSort: "display_order", tableColumns: ["label", "location", "href", "is_active"], searchFields: ["label", "href"], ...commonStatus,
    fields: [
      { name: "parent_id", label: "Parent ID", kind: "number" },
      { name: "label", label: "Label", kind: "text", required: true, table: true },
      { name: "icon", label: "Icon", kind: "text" },
      { name: "href", label: "Href", kind: "text", required: true, table: true },
      { name: "is_external", label: "External", kind: "boolean", filter: true },
      { name: "location", label: "Location", kind: "select", options: ["header", "footer", "mobile"], table: true, filter: true },
      { name: "is_mega_menu", label: "Mega Menu", kind: "boolean" },
      { name: "open_in_new_tab", label: "Open in New Tab", kind: "boolean" },
      { name: "authentication_required", label: "Authentication Required", kind: "boolean" },
      { name: "visible_roles", label: "Visible Roles", kind: "list" },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  footer: {
    module: "footer", title: "Footer", endpoint: "/footer", listEndpoint: "/footer/all", defaultSort: "updated_at", tableColumns: ["copyright_text", "newsletter_enabled", "is_active"], searchFields: ["copyright_text"], ...commonStatus,
    fields: [
      { name: "logo_url", label: "Logo", kind: "media", folder: "images", crop: true },
      { name: "description", label: "Description", kind: "richtext" },
      { name: "sections", label: "Sections", kind: "json" },
      { name: "quick_links", label: "Quick Links", kind: "json" },
      { name: "contact_details", label: "Contact Details", kind: "json" },
      { name: "social_links", label: "Social Links", kind: "json" },
      { name: "copyright_text", label: "Copyright Text", kind: "text", table: true },
      { name: "newsletter_enabled", label: "Newsletter Enabled", kind: "boolean", table: true, filter: true },
      { name: "newsletter_label", label: "Newsletter Label", kind: "text" },
      { name: "legal_links", label: "Legal Links", kind: "json" },
      { name: "display_order", label: "Display Order", kind: "number" },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  seo: {
    module: "seo", title: "SEO", endpoint: "/seo", defaultSort: "page_key", tableColumns: ["page_key", "meta_title", "robots_meta", "is_active"], searchFields: ["page_key", "meta_title"], ...commonStatus,
    fields: [
      { name: "page_key", label: "Page Key", kind: "text", required: true, table: true },
      { name: "site_title", label: "Site Title", kind: "text" },
      { name: "meta_title", label: "Meta Title", kind: "text", required: true, table: true },
      { name: "meta_description", label: "Meta Description", kind: "textarea" },
      { name: "meta_keywords", label: "Meta Keywords", kind: "list" },
      { name: "canonical_url", label: "Canonical URL", kind: "text" },
      { name: "robots_meta", label: "Robots Meta", kind: "text", table: true },
      { name: "open_graph", label: "Open Graph", kind: "json" },
      { name: "twitter_cards", label: "Twitter Cards", kind: "json" },
      { name: "hreflang", label: "Hreflang", kind: "json" },
      { name: "structured_data", label: "Structured Data", kind: "json" },
      { name: "sitemap_config", label: "Sitemap Config", kind: "json" },
      { name: "robots_txt", label: "Robots.txt", kind: "richtext" },
      { name: "verification_codes", label: "Verification Codes", kind: "json" },
      { name: "redirect_rules", label: "Redirect Rules", kind: "json" },
      { name: "favicon_url", label: "Favicon", kind: "media", folder: "images", crop: true },
      { name: "is_active", label: "Active", kind: "boolean", table: true, filter: true },
    ],
  },
  analytics: {
    module: "analytics", title: "Analytics", endpoint: "/analytics", defaultSort: "occurred_at", tableColumns: ["event_type", "occurred_at"], searchFields: ["event_type"],
    fields: [
      { name: "event_type", label: "Event Type", kind: "text", required: true, table: true, filter: true },
      { name: "occurred_at", label: "Occurred At", kind: "text", table: true },
      { name: "event_metadata", label: "Event Metadata", kind: "json" },
    ],
  },
};

export function moduleConfig(module: string) {
  return cmsModules[module] || cmsModules.content;
}

export function schemaFor(config: CmsModuleConfig) {
  const shape: Record<string, z.ZodTypeAny> = {};
  for (const field of config.fields) {
    let schema: z.ZodTypeAny;
    if (field.kind === "number") schema = z.coerce.number().optional().nullable();
    else if (field.kind === "boolean") schema = z.coerce.boolean().default(false);
    else if (field.kind === "list") schema = z.union([z.string(), z.array(z.string())]).optional();
    else if (field.kind === "json") schema = z.union([z.string(), z.record(z.any()), z.array(z.any())]).optional();
    else schema = z.string().optional();
    if (field.required && field.kind !== "boolean") schema = z.string().min(1, `${field.label} is required`);
    shape[field.name] = schema;
  }
  return z.object(shape);
}

export function normalizeValues(config: CmsModuleConfig, values: Record<string, unknown>) {
  const normalized: Record<string, unknown> = {};
  for (const field of config.fields) {
    const value = values[field.name];
    if (field.kind === "number") normalized[field.name] = value === "" || value == null ? null : Number(value);
    else if (field.kind === "boolean") normalized[field.name] = Boolean(value);
    else if (field.kind === "list") normalized[field.name] = Array.isArray(value) ? value : String(value || "").split(",").map((item) => item.trim()).filter(Boolean);
    else if (field.kind === "json") {
      if (typeof value === "string") normalized[field.name] = value.trim() ? JSON.parse(value) : {};
      else normalized[field.name] = value ?? {};
    } else normalized[field.name] = value ?? "";
  }
  return normalized;
}

export function defaultsFor(config: CmsModuleConfig) {
  return Object.fromEntries(config.fields.map((field) => {
    if (field.kind === "boolean") return [field.name, false];
    if (field.kind === "number") return [field.name, ""];
    if (field.kind === "list") return [field.name, ""];
    if (field.kind === "json") return [field.name, "{}"];
    if (field.kind === "select") return [field.name, field.options?.[0] || ""];
    return [field.name, ""];
  }));
}
