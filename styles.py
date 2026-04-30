"""
RootSync - Theme Configuration
Modern engineering dashboard color scheme and typography
"""

# =============================================================================
# COLOR PALETTE
# =============================================================================
COLORS = {
    # Primary backgrounds
    "bg_primary": "#FFFFFF",         # Main background
    "bg_secondary": "#FFFFFF",       # Panels/cards
    "bg_header": "#FFFFFF",          # Header bar
    "bg_control": "#FFFFFF",         # Control panel

    # Accent colors (minimal professional blue theme)
    "accent_primary": "#0F6CBD",     # Primary accent
    "accent_secondary": "#2B7CD3",   # Secondary accent
    "accent_hover": "#0959A5",       # Hover states
    "accent_light": "#EAF3FF",       # Very light highlight
    
    # Text colors
    "text_primary": "#111111",       # Main text
    "text_secondary": "#4B5563",     # Secondary text
    "text_muted": "#6B7280",         # Muted text
    "text_inverse": "#FFFFFF",       # White - on accent backgrounds
    
    # Status colors
    "success": "#16803C",            # Green - converged
    "success_bg": "#EAF7EE",         # Light green background
    "warning": "#B45309",            # Amber - not converged
    "warning_bg": "#FFF5E6",         # Light amber background
    "error": "#C53030",              # Red - error
    "error_bg": "#FDECEC",           # Light red background
    
    # Graph colors
    "graph_line": "#0F6CBD",         # Blue - function curve
    "graph_point": "#B45309",        # Amber - iteration points
    "graph_root": "#16803C",         # Green - root marker
    "graph_initial": "#6D28D9",      # Purple - initial guess
    "graph_grid": "#E5E7EB",         # Light gray - grid
    
    # Borders and dividers
    "border_light": "#E5E7EB",       # Light border
    "border_medium": "#CBD5E1",      # Medium border
    "shadow": "#111111",             # Shadow color (with alpha in use)
}

# =============================================================================
# TYPOGRAPHY
# =============================================================================
FONTS = {
    # Headers
    "title": ("Segoe UI", 22, "bold"),
    "subtitle": ("Segoe UI", 11),
    "section_header": ("Segoe UI", 11, "bold"),
    
    # Body
    "body": ("Segoe UI", 10),
    "body_bold": ("Segoe UI", 10, "bold"),
    "small": ("Segoe UI", 9),
    
    # Special
    "monospace": ("Consolas", 10),
    "monospace_small": ("Consolas", 9),
    "status_value": ("Segoe UI", 14, "bold"),
    "badge": ("Segoe UI", 9, "bold"),
    
    # Buttons
    "button": ("Segoe UI", 10),
    "button_primary": ("Segoe UI", 10, "bold"),
    
    # Labels
    "label": ("Segoe UI", 10),
    "entry": ("Segoe UI", 10),
}

# =============================================================================
# DIMENSIONS
# =============================================================================
DIMENSIONS = {
    # Window
    "window_width": 1280,
    "window_height": 800,
    "window_min_width": 1040,
    "window_min_height": 640,
    
    # Spacing
    "pad_xs": 4,
    "pad_sm": 8,
    "pad_md": 12,
    "pad_lg": 16,
    "pad_xl": 24,
    
    # Header
    "header_height": 60,
    
    # Control panel
    "control_height": 70,
    "entry_width": 14,
    
    # Graph
    "graph_min_width": 500,
    
    # Buttons
    "button_width": 12,
    "button_height": 2,
    
    # Border radius (simulated)
    "radius_sm": 4,
    "radius_md": 8,
    "radius_lg": 12,
}

# =============================================================================
# ANIMATION TIMING
# =============================================================================
ANIMATION = {
    "loading_interval": 100,         # ms between loading animation frames
    "hover_delay": 50,               # ms for hover effect
    "result_highlight_duration": 2000,  # ms to highlight result
}

# =============================================================================
# TTK STYLE CONFIGURATIONS
# =============================================================================
def apply_styles(style):
    """Apply modern theme to ttk widgets"""
    
    # Frames
    style.configure("TFrame", background=COLORS["bg_primary"])
    style.configure("Card.TFrame", background=COLORS["bg_secondary"])
    style.configure("Header.TFrame", background=COLORS["bg_header"])
    style.configure("Control.TFrame", background=COLORS["bg_control"])
    style.configure("Status.TFrame", background=COLORS["bg_secondary"])
    
    # Labels
    style.configure("TLabel", 
                    background=COLORS["bg_primary"], 
                    foreground=COLORS["text_primary"],
                    font=FONTS["body"])
    
    style.configure("Header.TLabel",
                    background=COLORS["bg_header"],
                    foreground=COLORS["text_primary"],
                    font=FONTS["title"])
    
    style.configure("HeaderSub.TLabel",
                    background=COLORS["bg_header"],
                    foreground=COLORS["text_secondary"],
                    font=FONTS["subtitle"])
    
    style.configure("Control.TLabel",
                    background=COLORS["bg_control"],
                    foreground=COLORS["text_primary"],
                    font=FONTS["label"])
    
    style.configure("Card.TLabel",
                    background=COLORS["bg_secondary"],
                    foreground=COLORS["text_primary"],
                    font=FONTS["body"])
    
    style.configure("SectionHeader.TLabel",
                    background=COLORS["bg_secondary"],
                    foreground=COLORS["accent_primary"],
                    font=FONTS["section_header"])
    
    style.configure("StatusTitle.TLabel",
                    background=COLORS["bg_secondary"],
                    foreground=COLORS["text_secondary"],
                    font=FONTS["small"])
    
    style.configure("StatusValue.TLabel",
                    background=COLORS["bg_secondary"],
                    foreground=COLORS["text_primary"],
                    font=FONTS["status_value"])
    
    # Success badge
    style.configure("Success.TLabel",
                    background=COLORS["success_bg"],
                    foreground=COLORS["success"],
                    font=FONTS["badge"])
    
    # Warning badge  
    style.configure("Warning.TLabel",
                    background=COLORS["warning_bg"],
                    foreground=COLORS["warning"],
                    font=FONTS["badge"])
    
    # Computing label
    style.configure("Computing.TLabel",
                    background=COLORS["bg_secondary"],
                    foreground=COLORS["accent_primary"],
                    font=FONTS["body_bold"])
    
    # LabelFrames
    style.configure("TLabelframe",
                    background=COLORS["bg_secondary"],
                    foreground=COLORS["text_primary"])
    
    style.configure("TLabelframe.Label",
                    background=COLORS["bg_secondary"],
                    foreground=COLORS["accent_primary"],
                    font=FONTS["section_header"])
    
    style.configure("Graph.TLabelframe",
                    background=COLORS["bg_secondary"])
    
    style.configure("Graph.TLabelframe.Label",
                    background=COLORS["bg_secondary"],
                    foreground=COLORS["accent_primary"],
                    font=FONTS["section_header"])
    
    style.configure("Trail.TLabelframe",
                    background=COLORS["bg_secondary"])
    
    style.configure("Trail.TLabelframe.Label",
                    background=COLORS["bg_secondary"],
                    foreground=COLORS["accent_primary"],
                    font=FONTS["section_header"])
    
    # Buttons - Primary (Calculate)
    style.configure("Primary.TButton",
                    font=FONTS["button_primary"],
                    padding=(16, 8),
                    borderwidth=0,
                    focusthickness=0)
    
    style.map("Primary.TButton",
              background=[("active", COLORS["accent_hover"]),
                         ("disabled", COLORS["border_light"]),
                         ("!disabled", COLORS["accent_primary"])],
              foreground=[("disabled", COLORS["text_muted"]),
                         ("!disabled", COLORS["text_inverse"])])
    
    # Buttons - Secondary (Clear)
    style.configure("Secondary.TButton",
                    font=FONTS["button"],
                    padding=(12, 8),
                    borderwidth=1,
                    focusthickness=0)
    
    style.map("Secondary.TButton",
              background=[("active", COLORS["border_medium"]),
                         ("!disabled", COLORS["bg_secondary"])],
              foreground=[("!disabled", COLORS["text_primary"])])
    
    # Entry fields
    style.configure("TEntry",
                    font=FONTS["entry"],
                    padding=6)
    
    # OptionMenu / Combobox
    style.configure("TMenubutton",
                    font=FONTS["body"],
                    padding=6)
    
    # Progressbar
    style.configure("Accent.Horizontal.TProgressbar",
                    troughcolor=COLORS["border_light"],
                    background=COLORS["accent_primary"],
                    thickness=4)
    
    # Separator
    style.configure("TSeparator",
                    background=COLORS["border_light"])


def get_graph_colors():
    """Return color configuration for matplotlib graph"""
    return {
        "figure_bg": COLORS["bg_secondary"],
        "axes_bg": COLORS["bg_secondary"],
        "line": COLORS["graph_line"],
        "points": COLORS["graph_point"],
        "root": COLORS["graph_root"],
        "initial": COLORS["graph_initial"],
        "grid": COLORS["graph_grid"],
        "text": COLORS["text_primary"],
        "axis": COLORS["text_secondary"],
    }
