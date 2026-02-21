"""
app.py  ─  Expertly Polished Contact Management System
UI/UX Reflected Version (Sleek Dark Mode, Optimised Grid, Micro-Aesthetics)
"""

import streamlit as st
from pathlib import Path
import base64
from cms import ContactManagementSystem
from photo_manager import PhotoManager

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CMS · Contacts",
    page_icon="👤",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Expert UI/UX Custom CSS Injection ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* global reset */
html, body, [class*="css"] { 
    font-family: 'Inter', sans-serif;
    background: #0a0a0a;
}

/* 1. NATIVE FEEL: Hide default Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
[data-testid="stToolbar"] { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stSidebarNav"] { display: none; }
[data-testid="collapsedControl"] { display: none; }

/* Adjust block container for native feel */
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 4rem;
    max-width: 900px;
}

/* 2. ENHANCED CONTACT CARDS */
.contact-card-container {
    background: linear-gradient(135deg, #1a1a1a 0%, #1e1e1e 100%);
    border: 1px solid #2d2d2d;
    border-radius: 16px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.4s ease-out;
    animation-fill-mode: both;
}
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.contact-card-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.contact-card-container:hover {
    border-color: #3a3a3a;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.05);
    transform: translateY(-2px);
}
.contact-card-container:hover::before {
    opacity: 1;
}

.avatar-circle {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.1rem;
    color: #ffffff;
    margin-right: 1.2rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    flex-shrink: 0;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}
.contact-card-container:hover .avatar-circle {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4) !important;
}

.contact-name {
    font-size: 1.15rem;
    font-weight: 600;
    color: #f5f5f5;
    line-height: 1.3;
    letter-spacing: -0.01em;
    margin-bottom: 0.3rem;
}
.contact-meta {
    font-size: 0.875rem;
    color: #999;
    margin-top: 2px;
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
}
.contact-meta span {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    color: #aaa;
    transition: color 0.2s ease;
}
.contact-meta span:hover {
    color: #fff;
}

/* 3. ENHANCED SEARCH INPUT */
.stTextInput > div > div > input {
    background-color: #151515 !important;
    border: 1.5px solid #2d2d2d !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
    color: #f0f0f0 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    background-color: #1a1a1a !important;
}
.stTextInput > div > div > input::placeholder {
    color: #666 !important;
}

/* 4. TABS BEAUTIFICATION */
[data-testid="stTabs"] [role="tablist"] {
    gap: 0.5rem;
    border-bottom: 1px solid #2d2d2d !important;
    margin-bottom: 1.5rem;
}
[data-testid="stTabs"] button[role="tab"] {
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    color: #666 !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    background: transparent !important;
    transition: all 0.2s ease !important;
    border-radius: 8px 8px 0 0 !important;
}
[data-testid="stTabs"] button[role="tab"]:hover {
    color: #aaa !important;
    background: rgba(255,255,255,0.02) !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #ffffff !important;
    border-bottom: 2px solid #667eea !important;
    background: rgba(102, 126, 234, 0.05) !important;
}

/* 5. ENHANCED INPUT FIELDS */
.stTextInput input, .stTextInput textarea {
    background-color: #151515 !important;
    border: 1.5px solid #2d2d2d !important;
    border-radius: 10px !important;
    color: #f0f0f0 !important;
    transition: all 0.3s ease !important;
}
.stTextInput input:focus, .stTextInput textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    background-color: #1a1a1a !important;
}
.stTextInput label {
    color: #aaa !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    margin-bottom: 0.5rem !important;
}

/* 6. ENHANCED BUTTONS */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
    border: none !important;
}
.stButton > button[type="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
}
.stButton > button[type="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
}
.stButton > button:not([type="primary"]) {
    background-color: #252525 !important;
    color: #f0f0f0 !important;
}
.stButton > button:not([type="primary"]):hover {
    background-color: #2d2d2d !important;
    transform: translateY(-1px);
}

/* 7. EXPANDER STYLING */
[data-testid="stExpander"] {
    border: 1px solid #2d2d2d !important;
    border-radius: 12px !important;
    background-color: #181818 !important;
    margin-top: 0.5rem;
}
[data-testid="stExpander"] summary {
    padding: 0.75rem 1rem !important;
    color: #aaa !important;
    font-weight: 500 !important;
}
[data-testid="stExpander"] summary:hover {
    color: #fff !important;
}

/* 8. HIDE INSTRUCTIONS */
[data-testid="InputInstructions"] { display: none !important; }
[data-testid="stForm"] p small { display: none !important; }
[data-testid="stForm"] > div[data-testid="stVerticalBlock"] > div:last-child { margin-bottom: -1rem !important; }

/* 9. DIVIDER */
hr {
    border-color: #2d2d2d !important;
    margin: 1.5rem 0 !important;
    opacity: 0.5;
}

/* 10. ENHANCED STATUS MESSAGES */
.stAlert {
    border-radius: 12px !important;
    border-left: 4px solid !important;
    padding: 1rem 1.25rem !important;
}
.stSuccess {
    background-color: rgba(16, 185, 129, 0.1) !important;
    border-left-color: #10b981 !important;
    color: #6ee7b7 !important;
}
.stError {
    background-color: rgba(239, 68, 68, 0.1) !important;
    border-left-color: #ef4444 !important;
    color: #fca5a5 !important;
}
.stWarning {
    background-color: rgba(245, 158, 11, 0.1) !important;
    border-left-color: #f59e0b !important;
    color: #fcd34d !important;
}
.stInfo {
    background-color: rgba(59, 130, 246, 0.1) !important;
    border-left-color: #3b82f6 !important;
    color: #93c5fd !important;
}

/* 11. EMPTY STATE */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #555;
}
.empty-state-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}
.empty-state-text {
    font-size: 1rem;
    color: #666;
    line-height: 1.6;
}

/* 12. SMOOTH SCROLLING */
html {
    scroll-behavior: smooth;
}

/* 13. STATS BADGE */
.stats-badge {
    display: inline-block;
    background: rgba(102, 126, 234, 0.1);
    color: #a5b4fc;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
    border: 1px solid rgba(102, 126, 234, 0.2);
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "cms" not in st.session_state:
    st.session_state.cms = ContactManagementSystem()
if "pending_delete" not in st.session_state:
    st.session_state.pending_delete = None  # phone of contact awaiting delete confirmation
if "photo_manager" not in st.session_state:
    st.session_state.photo_manager = PhotoManager()

cms: ContactManagementSystem = st.session_state.cms
photo_manager: PhotoManager = st.session_state.photo_manager

# ── App Header ────────────────────────────────────────────────────────────────
total_contacts = len(cms.view_contacts())
st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 1rem;">
    <div style="display: flex; align-items: center;">
        <div style="width: 48px; height: 48px; border-radius: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; margin-right: 1rem; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
            <span style="font-size: 1.5rem;">👤</span>
        </div>
        <div>
            <h1 style="font-size: 2.2rem; font-weight: 700; color: #fff; margin: 0; letter-spacing: -0.04em; background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Directory</h1>
            <p style="color: #888; font-size: 0.9rem; margin: 0.25rem 0 0 0;">Expertly managed personal contacts</p>
        </div>
    </div>
    <div class="stats-badge">{total_contacts} {'contact' if total_contacts == 1 else 'contacts'}</div>
</div>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def _get_initials(name: str) -> str:
    parts = name.strip().split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else name[:2].upper() or "?"

def _get_avatar_gradient(name: str) -> str:
    """Generate a consistent gradient color based on the contact's name."""
    # Use hash of name to pick from predefined gradient pairs
    gradients = [
        ("#667eea", "#764ba2"),  # Purple
        ("#f093fb", "#f5576c"),  # Pink-Red
        ("#4facfe", "#00f2fe"),  # Blue-Cyan
        ("#43e97b", "#38f9d7"),  # Green-Cyan
        ("#fa709a", "#fee140"),  # Pink-Yellow
        ("#30cfd0", "#330867"),  # Cyan-Purple
        ("#a8edea", "#fed6e3"),  # Light Cyan-Pink
        ("#ff9a9e", "#fecfef"),  # Coral-Pink
        ("#ffecd2", "#fcb69f"),  # Peach
        ("#ff8a80", "#ea6100"),  # Orange-Red
    ]
    hash_val = hash(name.lower()) % len(gradients)
    color1, color2 = gradients[hash_val]
    return f"linear-gradient(135deg, {color1} 0%, {color2} 100%)"

def _get_photo_base64(contact) -> str:
    """Get the photo as base64 data URI for a contact, or return empty string if no photo."""
    if not contact.photo:
        return ""
    photo_path = photo_manager.get_photo_path(contact.photo)
    if photo_path and photo_path.exists():
        try:
            with open(photo_path, "rb") as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data).decode()
                # Determine MIME type from extension
                ext = photo_path.suffix.lower()
                mime_types = {
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".png": "image/png",
                    ".webp": "image/webp",
                    ".gif": "image/gif",
                }
                mime_type = mime_types.get(ext, "image/jpeg")
                return f"data:{mime_type};base64,{img_base64}"
        except Exception:
            return ""
    return ""

# ── Navigation Tabs ───────────────────────────────────────────────────────────
tab_list, tab_create = st.tabs(["📋 All Contacts", "➕ Add New Contact"])

# ════════════════════════════════════════════════════════════════════════════ #
#  TAB 1: ALL CONTACTS (View, Search, Update, Delete)                          #
# ════════════════════════════════════════════════════════════════════════════ #
with tab_list:
    # Top Search Section
    search_query = st.text_input(
        "search", 
        placeholder="🔍 Search by name, phone, or email...", 
        label_visibility="collapsed"
    )
    
    # Grid separation
    st.divider()
    
    results = cms.search_contact(search_query)
    # Sort contacts alphabetically by name (case-insensitive)
    results = sorted(results, key=lambda c: c.name.lower())
    total_count = len(cms.view_contacts())
    
    if total_count == 0:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📇</div>
                <h3 style="color: #666; font-size: 1.25rem; font-weight: 600; margin-bottom: 0.5rem;">No contacts yet</h3>
                <p class="empty-state-text">Switch to the <strong style="color: #a5b4fc;">Add New Contact</strong> tab to create your first entry.</p>
            </div>
        """, unsafe_allow_html=True)
    elif not results:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h3 style="color: #666; font-size: 1.25rem; font-weight: 600; margin-bottom: 0.5rem;">No matches found</h3>
                <p class="empty-state-text">Try a different search term or check your spelling.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 0.5rem;">
                <p style='color: #888; font-size: 0.85rem; margin: 0;'>Showing <strong style="color: #a5b4fc;">{len(results)}</strong> of <strong style="color: #a5b4fc;">{total_count}</strong> {'contact' if total_count == 1 else 'contacts'}</p>
            </div>
        """, unsafe_allow_html=True)
        
        for idx, c in enumerate(results):
            # Contact Card Row
            with st.container():
                # Show email only when present; otherwise nothing (no extra div/space)
                contact_meta_parts = [f"<span>📞 {c.phone}</span>"]
                if c.email and c.email.strip():
                    contact_meta_parts.append(f"<span>✉️ {c.email.strip()}</span>")
                contact_meta_inner = "".join(contact_meta_parts)

                avatar_gradient = _get_avatar_gradient(c.name)
                animation_delay = idx * 0.05  # Stagger animation for each card
                photo_data_uri = _get_photo_base64(c)
                
                # Avatar: show photo if available, otherwise show initials with gradient
                if photo_data_uri:
                    avatar_html = f'<img src="{photo_data_uri}" style="width: 52px; height: 52px; border-radius: 50%; object-fit: cover; margin-right: 1.2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.3); flex-shrink: 0; border: 2px solid rgba(255,255,255,0.1);" />'
                else:
                    avatar_html = f'<div class="avatar-circle" style="background: {avatar_gradient}; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">{_get_initials(c.name)}</div>'
                
                st.markdown(f"""
                <div class="contact-card-container" style="animation-delay: {animation_delay}s;">
                    <div style="display: flex; align-items: center;">
                        {avatar_html}
                        <div style="flex-grow: 1;">
                            <div class="contact-name">{c.name}</div>
                            <div class="contact-meta">{contact_meta_inner}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Progressive Disclosure: Expandable Management
                with st.expander("⚙️ Manage Contact Details", expanded=False):
                    # Layout Optimization: Fields side-by-side
                    st.markdown("<p style='font-size: 0.875rem; color: #999; margin-bottom: 1.25rem; line-height: 1.6;'>Edit contact information or remove this entry from your directory.</p>", unsafe_allow_html=True)
                    
                    # Show current photo if available
                    current_photo_data = _get_photo_base64(c)
                    if current_photo_data:
                        st.markdown("<p style='font-size: 0.875rem; color: #999; margin-bottom: 0.5rem;'>Current photo:</p>", unsafe_allow_html=True)
                        st.markdown(f'<img src="{current_photo_data}" style="width: 100px; height: 100px; border-radius: 12px; object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.3);" />', unsafe_allow_html=True)
                    
                    # Native-like form for editing
                    with st.form(key=f"edit_form_{c.phone}"):
                        e_col1, e_col2, e_col3 = st.columns(3)
                        e_name = e_col1.text_input("Name", value=c.name, placeholder="👤 Full Name")
                        e_phone = e_col2.text_input("Phone", value=c.phone, placeholder="📞 10-digit number")
                        e_email = e_col3.text_input("Email", value=c.email, placeholder="✉️ Email address")
                        
                        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                        e_photo = st.file_uploader(
                            "Update Photo (Optional)",
                            type=["jpg", "jpeg", "png", "webp", "gif"],
                            key=f"edit_photo_{c.phone}",
                            help="Upload a new photo or leave empty to keep current photo"
                        )
                        
                        save_btn = st.form_submit_button("Save Changes", use_container_width=True, type="primary")
                        
                        if save_btn:
                            # Handle photo upload
                            new_photo_filename = c.photo  # Keep existing photo by default
                            if e_photo is not None:
                                # Delete old photo if exists
                                if c.photo:
                                    photo_manager.delete_photo(c.photo)
                                # Save new photo
                                saved_filename = photo_manager.save_photo(e_photo, e_phone)
                                if saved_filename:
                                    new_photo_filename = saved_filename
                            
                            success, msg = cms.update_contact(c.phone, e_name, e_phone, e_email, new_photo_filename)
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                    
                    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                    # Delete with confirmation: first click sets pending_delete, second confirms or cancels
                    if st.session_state.pending_delete == c.phone:
                        st.warning(f"Are you sure you want to delete **{c.name}**? This cannot be undone.")
                        confirm_col, cancel_col = st.columns(2)
                        with confirm_col:
                            if st.button("Yes, delete", key=f"confirm_del_{c.phone}", type="primary", use_container_width=True):
                                # Delete photo if exists
                                if c.photo:
                                    photo_manager.delete_photo(c.photo)
                                success, msg = cms.delete_contact(c.phone)
                                st.session_state.pending_delete = None
                                if success:
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                        with cancel_col:
                            if st.button("Cancel", key=f"cancel_del_{c.phone}", use_container_width=True):
                                st.session_state.pending_delete = None
                                st.rerun()
                    else:
                        if st.button(f"🗑️ Delete {c.name}", key=f"del_btn_{c.phone}", use_container_width=True):
                            # Delete photo if exists
                            if c.photo:
                                photo_manager.delete_photo(c.photo)
                            st.session_state.pending_delete = c.phone
                            st.rerun()


# ════════════════════════════════════════════════════════════════════════════ #
#  TAB 2: ADD NEW CONTACT                                                     #
# ════════════════════════════════════════════════════════════════════════════ #
with tab_create:
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h2 style="font-size: 1.5rem; font-weight: 600; color: #f0f0f0; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.75rem;">➕</span> Create New Contact
            </h2>
            <p style='color: #999; font-size: 0.9rem; line-height: 1.6; margin: 0;'>Add a new contact to your directory. Phone number must be exactly 10 digits (optional +91 prefix).</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("new_contact_form", clear_on_submit=True):
        # Layout Optimization: Input fields side-by-side
        col1, col2, col3 = st.columns(3)
        
        new_name = col1.text_input("Full Name", placeholder="👤 e.g. John Doe")
        new_phone = col2.text_input("Phone Number", placeholder="📞 e.g. 9876543210")
        new_email = col3.text_input("Email (Optional)", placeholder="✉️ e.g. john@example.com")
        
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        new_photo = st.file_uploader(
            "Photo (Optional)",
            type=["jpg", "jpeg", "png", "webp", "gif"],
            key="new_contact_photo",
            help="Upload a photo for this contact"
        )
        
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        add_submit = st.form_submit_button("Create Contact", use_container_width=True, type="primary")
        
    if add_submit:
        # Handle photo upload
        photo_filename = ""
        if new_photo is not None:
            saved_filename = photo_manager.save_photo(new_photo, new_phone)
            if saved_filename:
                photo_filename = saved_filename
        
        success, msg = cms.add_contact(new_name, new_phone, new_email, photo_filename)
        if success:
            st.success(msg)
            st.rerun()  # refresh so new contact appears in "All Contacts" immediately
        else:
            st.error(msg)
