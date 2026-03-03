"""
RootSync - Modern UI/UX Layer
Engineering dashboard interface for Newton-Raphson root finder
"""

import sys
import platform
from datetime import datetime
import tkinter as tk
from tkinter import ttk

# Import solver logic
from solver import FUNCTIONS, newton_raphson, validate_inputs

# Import theme configuration
from styles import (
    COLORS, FONTS, DIMENSIONS, ANIMATION,
    apply_styles, get_graph_colors
)

# Matplotlib import with fallback
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib
    matplotlib.use('TkAgg')
    MATPLOTLIB_OK = True
except Exception:
    MATPLOTLIB_OK = False


class RootSyncApp:
    """Modern engineering dashboard for Newton-Raphson root finding"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.setup_variables()
        self.create_ui()
        self.is_computing = False
        self.loading_animation_id = None
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("RootSync")
        self.root.geometry(f"{DIMENSIONS['window_width']}x{DIMENSIONS['window_height']}")
        self.root.minsize(DIMENSIONS['window_min_width'], DIMENSIONS['window_min_height'])
        self.root.configure(bg=COLORS['bg_primary'])
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - DIMENSIONS['window_width']) // 2
        y = (self.root.winfo_screenheight() - DIMENSIONS['window_height']) // 2
        self.root.geometry(f"+{x}+{y}")
        
    def setup_styles(self):
        """Initialize ttk styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam as base for better customization
        apply_styles(self.style)
        
    def setup_variables(self):
        """Initialize tkinter variables"""
        self.func_var = tk.StringVar(value=list(FUNCTIONS.keys())[0])
        self.status_var = tk.StringVar(value="Ready")
        self.root_var = tk.StringVar(value="—")
        self.iterations_var = tk.StringVar(value="—")
        self.convergence_var = tk.StringVar(value="—")
        self.loading_dots = 0
        
    def create_ui(self):
        """Create the main UI layout"""
        # Main container
        self.main_container = tk.Frame(self.root, bg=COLORS['bg_primary'])
        self.main_container.pack(fill='both', expand=True)
        
        # Create sections
        self.create_header()
        self.create_control_panel()
        self.create_status_panel()
        self.create_main_content()
        
    # =========================================================================
    # HEADER SECTION
    # =========================================================================
    def create_header(self):
        """Create the dark header bar"""
        header = tk.Frame(self.main_container, bg=COLORS['bg_header'], height=DIMENSIONS['header_height'])
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Inner padding container
        header_inner = tk.Frame(header, bg=COLORS['bg_header'])
        header_inner.pack(fill='both', expand=True, padx=DIMENSIONS['pad_xl'], pady=DIMENSIONS['pad_md'])
        
        # App title
        title_frame = tk.Frame(header_inner, bg=COLORS['bg_header'])
        title_frame.pack(side='left', fill='y')
        
        title = tk.Label(
            title_frame,
            text="RootSync",
            font=FONTS['title'],
            bg=COLORS['bg_header'],
            fg=COLORS['text_inverse']
        )
        title.pack(side='left')
        
        # Accent dot
        dot = tk.Label(
            title_frame,
            text=" •",
            font=FONTS['title'],
            bg=COLORS['bg_header'],
            fg=COLORS['accent_secondary']
        )
        dot.pack(side='left')
        
        # Subtitle
        subtitle = tk.Label(
            header_inner,
            text="Newton-Raphson Visual Root Finder",
            font=FONTS['subtitle'],
            bg=COLORS['bg_header'],
            fg=COLORS['text_muted']
        )
        subtitle.pack(side='left', padx=(DIMENSIONS['pad_lg'], 0))
        
        # Version badge on right
        version_frame = tk.Frame(header_inner, bg=COLORS['bg_header'])
        version_frame.pack(side='right')
        
        version = tk.Label(
            version_frame,
            text="v2.0",
            font=FONTS['small'],
            bg=COLORS['accent_primary'],
            fg=COLORS['text_inverse'],
            padx=8,
            pady=2
        )
        version.pack()
        
    # =========================================================================
    # CONTROL PANEL
    # =========================================================================
    def create_control_panel(self):
        """Create the control panel with inputs and buttons"""
        control_container = tk.Frame(self.main_container, bg=COLORS['bg_primary'])
        control_container.pack(fill='x', padx=DIMENSIONS['pad_xl'], pady=(DIMENSIONS['pad_lg'], 0))
        
        control_panel = tk.Frame(control_container, bg=COLORS['bg_control'])
        control_panel.pack(fill='x')
        
        # Inner content with padding
        control_inner = tk.Frame(control_panel, bg=COLORS['bg_control'])
        control_inner.pack(fill='x', padx=DIMENSIONS['pad_lg'], pady=DIMENSIONS['pad_md'])
        
        # Function selector
        func_frame = tk.Frame(control_inner, bg=COLORS['bg_control'])
        func_frame.pack(side='left', padx=(0, DIMENSIONS['pad_xl']))
        
        tk.Label(
            func_frame,
            text="Function",
            font=FONTS['small'],
            bg=COLORS['bg_control'],
            fg=COLORS['text_secondary']
        ).pack(anchor='w')
        
        self.func_menu = ttk.OptionMenu(
            func_frame,
            self.func_var,
            self.func_var.get(),
            *FUNCTIONS.keys()
        )
        self.func_menu.config(width=20)
        self.func_menu.pack(anchor='w', pady=(2, 0))
        
        # Initial guess (x0)
        x0_frame = tk.Frame(control_inner, bg=COLORS['bg_control'])
        x0_frame.pack(side='left', padx=(0, DIMENSIONS['pad_lg']))
        
        tk.Label(
            x0_frame,
            text="Initial Guess (x₀)",
            font=FONTS['small'],
            bg=COLORS['bg_control'],
            fg=COLORS['text_secondary']
        ).pack(anchor='w')
        
        self.x0_entry = ttk.Entry(x0_frame, width=DIMENSIONS['entry_width'], font=FONTS['entry'])
        self.x0_entry.pack(anchor='w', pady=(2, 0))
        self.x0_entry.insert(0, "1.5")
        
        # Tolerance
        tol_frame = tk.Frame(control_inner, bg=COLORS['bg_control'])
        tol_frame.pack(side='left', padx=(0, DIMENSIONS['pad_lg']))
        
        tk.Label(
            tol_frame,
            text="Tolerance (ε)",
            font=FONTS['small'],
            bg=COLORS['bg_control'],
            fg=COLORS['text_secondary']
        ).pack(anchor='w')
        
        self.tol_entry = ttk.Entry(tol_frame, width=DIMENSIONS['entry_width'], font=FONTS['entry'])
        self.tol_entry.pack(anchor='w', pady=(2, 0))
        self.tol_entry.insert(0, "0.0001")
        
        # Max iterations
        iter_frame = tk.Frame(control_inner, bg=COLORS['bg_control'])
        iter_frame.pack(side='left', padx=(0, DIMENSIONS['pad_xl']))
        
        tk.Label(
            iter_frame,
            text="Max Iterations",
            font=FONTS['small'],
            bg=COLORS['bg_control'],
            fg=COLORS['text_secondary']
        ).pack(anchor='w')
        
        self.iter_entry = ttk.Entry(iter_frame, width=DIMENSIONS['entry_width'], font=FONTS['entry'])
        self.iter_entry.pack(anchor='w', pady=(2, 0))
        self.iter_entry.insert(0, "20")
        
        # Buttons frame (right side)
        buttons_frame = tk.Frame(control_inner, bg=COLORS['bg_control'])
        buttons_frame.pack(side='right')
        
        # Clear button
        self.clear_btn = tk.Button(
            buttons_frame,
            text="Clear",
            font=FONTS['button'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            activebackground=COLORS['border_medium'],
            activeforeground=COLORS['text_primary'],
            relief='flat',
            cursor='hand2',
            padx=16,
            pady=6,
            command=self.clear
        )
        self.clear_btn.pack(side='left', padx=(0, DIMENSIONS['pad_sm']))
        self.bind_hover_effect(self.clear_btn, COLORS['border_light'], COLORS['bg_secondary'])
        
        # Calculate button
        self.calc_btn = tk.Button(
            buttons_frame,
            text="Calculate",
            font=FONTS['button_primary'],
            bg=COLORS['accent_primary'],
            fg=COLORS['text_inverse'],
            activebackground=COLORS['accent_hover'],
            activeforeground=COLORS['text_inverse'],
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=6,
            command=self.compute
        )
        self.calc_btn.pack(side='left')
        self.bind_hover_effect(self.calc_btn, COLORS['accent_hover'], COLORS['accent_primary'])
        
    def bind_hover_effect(self, widget, hover_color, normal_color):
        """Bind hover effects to a widget"""
        widget.bind('<Enter>', lambda e: widget.config(bg=hover_color))
        widget.bind('<Leave>', lambda e: widget.config(bg=normal_color))
        
    # =========================================================================
    # STATUS PANEL
    # =========================================================================
    def create_status_panel(self):
        """Create the status panel with result indicators"""
        status_container = tk.Frame(self.main_container, bg=COLORS['bg_primary'])
        status_container.pack(fill='x', padx=DIMENSIONS['pad_xl'], pady=DIMENSIONS['pad_md'])
        
        status_panel = tk.Frame(status_container, bg=COLORS['bg_secondary'])
        status_panel.pack(fill='x')
        
        # Inner content
        status_inner = tk.Frame(status_panel, bg=COLORS['bg_secondary'])
        status_inner.pack(fill='x', padx=DIMENSIONS['pad_lg'], pady=DIMENSIONS['pad_md'])
        
        # Root value
        root_frame = tk.Frame(status_inner, bg=COLORS['bg_secondary'])
        root_frame.pack(side='left', padx=(0, DIMENSIONS['pad_xl'] * 2))
        
        tk.Label(
            root_frame,
            text="ROOT ESTIMATE",
            font=FONTS['small'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_secondary']
        ).pack(anchor='w')
        
        self.root_label = tk.Label(
            root_frame,
            textvariable=self.root_var,
            font=FONTS['status_value'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        )
        self.root_label.pack(anchor='w')
        
        # Iterations
        iter_frame = tk.Frame(status_inner, bg=COLORS['bg_secondary'])
        iter_frame.pack(side='left', padx=(0, DIMENSIONS['pad_xl'] * 2))
        
        tk.Label(
            iter_frame,
            text="ITERATIONS",
            font=FONTS['small'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_secondary']
        ).pack(anchor='w')
        
        self.iter_label = tk.Label(
            iter_frame,
            textvariable=self.iterations_var,
            font=FONTS['status_value'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary']
        )
        self.iter_label.pack(anchor='w')
        
        # Convergence status
        conv_frame = tk.Frame(status_inner, bg=COLORS['bg_secondary'])
        conv_frame.pack(side='left', padx=(0, DIMENSIONS['pad_xl'] * 2))
        
        tk.Label(
            conv_frame,
            text="STATUS",
            font=FONTS['small'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_secondary']
        ).pack(anchor='w')
        
        self.badge_frame = tk.Frame(conv_frame, bg=COLORS['bg_secondary'])
        self.badge_frame.pack(anchor='w', pady=(2, 0))
        
        self.convergence_badge = tk.Label(
            self.badge_frame,
            text="Ready",
            font=FONTS['badge'],
            bg=COLORS['border_light'],
            fg=COLORS['text_secondary'],
            padx=10,
            pady=3
        )
        self.convergence_badge.pack()
        
        # Loading indicator (hidden by default)
        self.loading_frame = tk.Frame(status_inner, bg=COLORS['bg_secondary'])
        self.loading_frame.pack(side='right')
        
        self.loading_label = tk.Label(
            self.loading_frame,
            text="",
            font=FONTS['body_bold'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['accent_primary']
        )
        self.loading_label.pack()
        
        # Progress bar (hidden by default)
        self.progress = ttk.Progressbar(
            self.loading_frame,
            style="Accent.Horizontal.TProgressbar",
            mode='indeterminate',
            length=150
        )
        
    # =========================================================================
    # MAIN CONTENT (Graph + Solution Trail)
    # =========================================================================
    def create_main_content(self):
        """Create the split layout with graph and solution trail"""
        content = tk.Frame(self.main_container, bg=COLORS['bg_primary'])
        content.pack(fill='both', expand=True, padx=DIMENSIONS['pad_xl'], pady=(0, DIMENSIONS['pad_xl']))
        
        # Configure grid weights for split
        content.columnconfigure(0, weight=3)  # Graph gets more space
        content.columnconfigure(1, weight=2)  # Trail gets less
        content.rowconfigure(0, weight=1)
        
        # Left: Graph panel
        self.create_graph_panel(content)
        
        # Right: Solution trail panel
        self.create_trail_panel(content)
        
    def create_graph_panel(self, parent):
        """Create the graph panel"""
        graph_outer = tk.Frame(parent, bg=COLORS['bg_secondary'])
        graph_outer.grid(row=0, column=0, sticky='nsew', padx=(0, DIMENSIONS['pad_md']))
        
        # Header
        graph_header = tk.Frame(graph_outer, bg=COLORS['bg_secondary'])
        graph_header.pack(fill='x', padx=DIMENSIONS['pad_md'], pady=(DIMENSIONS['pad_md'], 0))
        
        tk.Label(
            graph_header,
            text="📈  Function Graph",
            font=FONTS['section_header'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['accent_primary']
        ).pack(side='left')
        
        # Graph area
        graph_content = tk.Frame(graph_outer, bg=COLORS['bg_secondary'])
        graph_content.pack(fill='both', expand=True, padx=DIMENSIONS['pad_sm'], pady=DIMENSIONS['pad_sm'])
        
        if MATPLOTLIB_OK:
            colors = get_graph_colors()
            
            self.fig = Figure(figsize=(6, 4), dpi=100, facecolor=colors['figure_bg'])
            self.ax = self.fig.add_subplot(111)
            self.ax.set_facecolor(colors['axes_bg'])
            self.ax.grid(True, color=colors['grid'], linestyle='-', linewidth=0.5, alpha=0.7)
            self.ax.tick_params(colors=colors['axis'])
            for spine in self.ax.spines.values():
                spine.set_color(colors['grid'])
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=graph_content)
            self.canvas.get_tk_widget().pack(fill='both', expand=True)
        else:
            no_graph = tk.Label(
                graph_content,
                text="📉  Graph unavailable\n\nInstall matplotlib:\npip install matplotlib",
                font=FONTS['body'],
                bg=COLORS['bg_secondary'],
                fg=COLORS['text_muted'],
                justify='center'
            )
            no_graph.pack(expand=True)
            self.fig = None
            self.ax = None
            self.canvas = None
            
    def create_trail_panel(self, parent):
        """Create the solution trail panel"""
        trail_outer = tk.Frame(parent, bg=COLORS['bg_secondary'])
        trail_outer.grid(row=0, column=1, sticky='nsew')
        
        # Header
        trail_header = tk.Frame(trail_outer, bg=COLORS['bg_secondary'])
        trail_header.pack(fill='x', padx=DIMENSIONS['pad_md'], pady=(DIMENSIONS['pad_md'], 0))
        
        tk.Label(
            trail_header,
            text="📋  Solution Trail",
            font=FONTS['section_header'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['accent_primary']
        ).pack(side='left')
        
        # Trail content with custom text widget
        trail_content = tk.Frame(trail_outer, bg=COLORS['bg_secondary'])
        trail_content.pack(fill='both', expand=True, padx=DIMENSIONS['pad_sm'], pady=DIMENSIONS['pad_sm'])
        
        # Create text widget with scrollbar
        self.trail = tk.Text(
            trail_content,
            wrap=tk.WORD,
            font=FONTS['monospace'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_primary'],
            relief='flat',
            padx=12,
            pady=12,
            spacing1=2,
            spacing2=1,
            spacing3=2
        )
        
        scrollbar = ttk.Scrollbar(trail_content, orient='vertical', command=self.trail.yview)
        self.trail.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        self.trail.pack(side='left', fill='both', expand=True)
        
        # Configure text tags for styling
        self.configure_trail_tags()
        
    def configure_trail_tags(self):
        """Configure text tags for solution trail styling"""
        # Section headers
        self.trail.tag_configure("section", 
            font=FONTS['section_header'],
            foreground=COLORS['accent_primary'],
            spacing1=12,
            spacing3=4
        )
        
        # Sub-headers
        self.trail.tag_configure("subheader",
            font=FONTS['body_bold'],
            foreground=COLORS['text_primary']
        )
        
        # Normal text
        self.trail.tag_configure("normal",
            font=FONTS['monospace'],
            foreground=COLORS['text_primary']
        )
        
        # Muted text
        self.trail.tag_configure("muted",
            font=FONTS['monospace_small'],
            foreground=COLORS['text_muted']
        )
        
        # Table header
        self.trail.tag_configure("table_header",
            font=FONTS['monospace'],
            foreground=COLORS['text_secondary'],
            background=COLORS['bg_control']
        )
        
        # Table row
        self.trail.tag_configure("table_row",
            font=FONTS['monospace_small'],
            foreground=COLORS['text_primary']
        )
        
        # Success (final answer highlight)
        self.trail.tag_configure("success",
            font=FONTS['body_bold'],
            foreground=COLORS['success'],
            background=COLORS['success_bg']
        )
        
        # Warning
        self.trail.tag_configure("warning",
            font=FONTS['body_bold'],
            foreground=COLORS['warning'],
            background=COLORS['warning_bg']
        )
        
        # Divider
        self.trail.tag_configure("divider",
            foreground=COLORS['border_light'],
            font=FONTS['monospace_small']
        )
        
    # =========================================================================
    # COMPUTATION
    # =========================================================================
    def compute(self):
        """Run Newton-Raphson computation"""
        if self.is_computing:
            return
            
        # Clear and reset
        self.trail.delete("1.0", tk.END)
        self.reset_status()
        
        # Start loading animation
        self.start_loading()
        
        # Validate inputs
        ok, data, err = validate_inputs(
            self.x0_entry.get(),
            self.tol_entry.get(),
            self.iter_entry.get()
        )
        
        # Log validation
        self.insert_section("VALIDATION")
        
        if not ok:
            self.trail.insert(tk.END, f"Status: FAIL\n", "warning")
            self.trail.insert(tk.END, f"Reason: {err}\n", "normal")
            self.stop_loading()
            self.set_badge("Error", "error")
            return
        else:
            self.trail.insert(tk.END, "Status: PASS ✓\n\n", "success")
            
        # Schedule computation to allow UI update
        self.root.after(100, lambda: self.run_computation(data))
        
    def run_computation(self, data):
        """Execute the Newton-Raphson solver"""
        func_name = self.func_var.get()
        f, df = FUNCTIONS[func_name]
        
        x0 = data["x0"]
        tol = data["tol"]
        max_iter = data["max_iter"]
        
        # Run solver
        result = newton_raphson(f, df, x0, tol, max_iter)
        
        # Build solution trail
        self.build_solution_trail(func_name, x0, tol, max_iter, result)
        
        # Update status panel
        self.update_status(result)
        
        # Plot graph
        if MATPLOTLIB_OK:
            self.plot_function(func_name, f, result, x0)
            
        # Stop loading
        self.stop_loading()
        
    def build_solution_trail(self, func_name, x0, tol, max_iter, result):
        """Build the formatted solution trail"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pyver = sys.version.split()[0]
        
        # GIVEN section
        self.insert_section("GIVEN")
        self.trail.insert(tk.END, f"Function:        {func_name}\n", "normal")
        self.trail.insert(tk.END, f"Initial Guess:   x₀ = {x0:.6f}\n", "normal")
        self.trail.insert(tk.END, f"Tolerance:       ε = {tol}\n", "normal")
        self.trail.insert(tk.END, f"Max Iterations:  {max_iter}\n\n", "normal")
        
        # METHOD section
        self.insert_section("METHOD")
        self.trail.insert(tk.END, "Newton-Raphson Iteration\n", "subheader")
        self.trail.insert(tk.END, "Formula: x_{n+1} = x_n - f(x_n) / f'(x_n)\n", "muted")
        self.trail.insert(tk.END, "Stop when: |Δx| < ε\n\n", "muted")
        
        # STEPS section
        self.insert_section("STEPS")
        
        # Table header
        header = " n │     x_n      │    f(x_n)    │   f'(x_n)    │   x_{n+1}    │    |Δx|    \n"
        divider = "───┼──────────────┼──────────────┼──────────────┼──────────────┼────────────\n"
        
        self.trail.insert(tk.END, header, "table_header")
        self.trail.insert(tk.END, divider, "divider")
        
        for row in result["rows"]:
            line = (
                f"{row['n']:>2} │ "
                f"{row['x_n']:>12.6f} │ "
                f"{row['f_x']:>12.6f} │ "
                f"{row['df_x']:>12.6f} │ "
                f"{row['x_next']:>12.6f} │ "
                f"{row['dx']:>10.6f}\n"
            )
            self.trail.insert(tk.END, line, "table_row")
            
        self.trail.insert(tk.END, "\n", "normal")
        
        # FINAL ANSWER section
        self.insert_section("FINAL ANSWER")
        
        root_est = result["root"]
        converged = result["converged"]
        it_used = result["iterations"]
        
        if converged:
            self.trail.insert(tk.END, f"  Root estimate: x ≈ {root_est:.6f}  \n", "success")
        else:
            self.trail.insert(tk.END, f"  Root estimate: x ≈ {root_est:.6f}  \n", "warning")
            
        self.trail.insert(tk.END, f"\nConverged:       {'YES ✓' if converged else 'NO ✗'}\n", "normal")
        self.trail.insert(tk.END, f"Iterations:      {it_used}\n", "normal")
        self.trail.insert(tk.END, f"Stop reason:     {result['stop_reason']}\n\n", "muted")
        
        # VERIFICATION section
        self.insert_section("VERIFICATION")
        self.trail.insert(tk.END, f"Residual: |f(x)| = {result['residual']:.6e}\n", "normal")
        
        if converged:
            self.trail.insert(tk.END, "Conclusion: Valid within tolerance ✓\n\n", "success")
        else:
            self.trail.insert(tk.END, "Conclusion: Not within tolerance. Consider adjusting x₀ or max iterations.\n\n", "warning")
            
        # SUMMARY section
        self.insert_section("SUMMARY")
        self.trail.insert(tk.END, f"Timestamp:  {timestamp}\n", "muted")
        self.trail.insert(tk.END, f"Python:     {pyver}\n", "muted")
        self.trail.insert(tk.END, f"Platform:   {platform.system()} {platform.release()}\n", "muted")
        self.trail.insert(tk.END, f"Graph:      {'Enabled' if MATPLOTLIB_OK else 'Disabled'}\n", "muted")
        
    def insert_section(self, title):
        """Insert a styled section header"""
        self.trail.insert(tk.END, f"{'─' * 50}\n", "divider")
        self.trail.insert(tk.END, f"  {title}\n", "section")
        self.trail.insert(tk.END, f"{'─' * 50}\n", "divider")
        
    # =========================================================================
    # STATUS UPDATES
    # =========================================================================
    def reset_status(self):
        """Reset status panel to initial state"""
        self.root_var.set("—")
        self.iterations_var.set("—")
        self.set_badge("Computing...", "computing")
        
    def update_status(self, result):
        """Update status panel with results"""
        self.root_var.set(f"x ≈ {result['root']:.6f}")
        self.iterations_var.set(str(result['iterations']))
        
        if result['converged']:
            self.set_badge("Converged", "success")
        else:
            self.set_badge("Not Converged", "warning")
            
    def set_badge(self, text, badge_type):
        """Set convergence badge style"""
        if badge_type == "success":
            bg = COLORS['success_bg']
            fg = COLORS['success']
        elif badge_type == "warning":
            bg = COLORS['warning_bg']
            fg = COLORS['warning']
        elif badge_type == "error":
            bg = COLORS['error_bg']
            fg = COLORS['error']
        elif badge_type == "computing":
            bg = COLORS['accent_light']
            fg = COLORS['accent_primary']
        else:
            bg = COLORS['border_light']
            fg = COLORS['text_secondary']
            
        self.convergence_badge.config(text=text, bg=bg, fg=fg)
        
    # =========================================================================
    # LOADING ANIMATION
    # =========================================================================
    def start_loading(self):
        """Start loading animation and disable calculate button"""
        self.is_computing = True
        self.calc_btn.config(state='disabled', bg=COLORS['border_light'], cursor='wait')
        self.clear_btn.config(state='disabled')
        
        # Show progress bar
        self.progress.pack(pady=(4, 0))
        self.progress.start(10)
        
        # Start loading text animation
        self.loading_dots = 0
        self.animate_loading()
        
    def animate_loading(self):
        """Animate the loading text"""
        if not self.is_computing:
            return
            
        dots = "." * (self.loading_dots % 4)
        self.loading_label.config(text=f"Computing{dots}")
        self.loading_dots += 1
        
        self.loading_animation_id = self.root.after(
            ANIMATION['loading_interval'] * 3,
            self.animate_loading
        )
        
    def stop_loading(self):
        """Stop loading animation and re-enable buttons"""
        self.is_computing = False
        
        if self.loading_animation_id:
            self.root.after_cancel(self.loading_animation_id)
            self.loading_animation_id = None
            
        self.loading_label.config(text="")
        self.progress.stop()
        self.progress.pack_forget()
        
        self.calc_btn.config(
            state='normal',
            bg=COLORS['accent_primary'],
            cursor='hand2'
        )
        self.clear_btn.config(state='normal')
        
    # =========================================================================
    # PLOTTING
    # =========================================================================
    def plot_function(self, func_name, f, result, x0):
        """Plot the function with iteration points"""
        colors = get_graph_colors()
        
        self.ax.clear()
        self.ax.set_facecolor(colors['axes_bg'])
        self.ax.grid(True, color=colors['grid'], linestyle='-', linewidth=0.5, alpha=0.7)
        
        root_est = result['root']
        rows = result['rows']
        
        # Determine x range
        center = (x0 + root_est) / 2.0
        span = max(2.0, abs(root_est - x0) * 4.0)
        x_min = center - span
        x_max = center + span
        
        if x_min == x_max:
            x_min -= 2
            x_max += 2
            
        # Generate curve points
        xs = []
        ys = []
        steps = 400
        for i in range(steps + 1):
            x = x_min + (x_max - x_min) * (i / steps)
            try:
                y = f(x)
            except Exception:
                y = float("nan")
            xs.append(x)
            ys.append(y)
            
        # Plot function curve
        self.ax.plot(xs, ys, color=colors['line'], linewidth=2.5, label='f(x)')
        
        # Plot x-axis
        self.ax.axhline(0, color=colors['axis'], linewidth=1)
        
        # Plot initial guess
        try:
            self.ax.scatter(
                [x0], [f(x0)],
                s=80, color=colors['initial'],
                marker='o', zorder=5,
                label=f'x₀ = {x0:.2f}'
            )
        except Exception:
            pass
            
        # Plot iteration points
        if rows:
            iter_xs = [r["x_n"] for r in rows]
            iter_ys = [r["f_x"] for r in rows]
            self.ax.scatter(
                iter_xs, iter_ys,
                s=40, color=colors['points'],
                marker='o', alpha=0.8, zorder=4,
                label='Iterations'
            )
            
        # Plot root estimate
        self.ax.scatter(
            [root_est], [0],
            s=120, color=colors['root'],
            marker='X', zorder=6,
            label=f'Root ≈ {root_est:.4f}'
        )
        
        # Style axes
        self.ax.set_xlabel("x", fontsize=10, color=colors['text'])
        self.ax.set_ylabel("f(x)", fontsize=10, color=colors['text'])
        self.ax.set_title(func_name, fontsize=11, fontweight='bold', color=colors['text'], pad=10)
        
        # Legend
        self.ax.legend(loc='best', fontsize=8, framealpha=0.9)
        
        # Adjust tick colors
        self.ax.tick_params(colors=colors['axis'], labelsize=9)
        for spine in self.ax.spines.values():
            spine.set_color(colors['grid'])
            
        self.fig.tight_layout()
        self.canvas.draw()
        
    # =========================================================================
    # CLEAR
    # =========================================================================
    def clear(self):
        """Reset all inputs and outputs"""
        # Clear trail
        self.trail.delete("1.0", tk.END)
        
        # Reset status
        self.root_var.set("—")
        self.iterations_var.set("—")
        self.set_badge("Ready", "default")
        
        # Reset inputs to defaults
        self.x0_entry.delete(0, tk.END)
        self.tol_entry.delete(0, tk.END)
        self.iter_entry.delete(0, tk.END)
        
        self.x0_entry.insert(0, "1.5")
        self.tol_entry.insert(0, "0.0001")
        self.iter_entry.insert(0, "20")
        
        # Clear graph
        if MATPLOTLIB_OK and self.ax:
            colors = get_graph_colors()
            self.ax.clear()
            self.ax.set_facecolor(colors['axes_bg'])
            self.ax.grid(True, color=colors['grid'], linestyle='-', linewidth=0.5, alpha=0.7)
            self.ax.set_xlabel("x", fontsize=10, color=colors['text'])
            self.ax.set_ylabel("f(x)", fontsize=10, color=colors['text'])
            self.canvas.draw()
