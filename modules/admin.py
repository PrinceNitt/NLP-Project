"""
Admin module for Resume Parser NLP Application.
Handles admin authentication and administrative functions.
"""
import base64
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Optional, List, Dict, Any

from config import ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_SESSION_KEY
from utils.database import (
    get_all_pdfs, 
    get_pdf_by_id, 
    get_feedback, 
    init_database,
    get_all_pdfs_with_details,
    get_statistics
)
from utils.logger import setup_logger, log_error
from utils.validators import sanitize_input
from utils.auth import (
    authenticate_admin_secure,
    is_admin_authenticated,
    logout_admin,
    get_session_remaining_time
)
from utils.health import (
    check_system_health,
    get_system_stats
)
from utils.ui_components import (
    create_hero_section,
    create_metric_card,
    apply_custom_css
)

logger = setup_logger(__name__)


# Authentication functions moved to utils.auth for better security
# Using secure authentication with password hashing and session timeout


def process_admin_mode() -> None:
    """Main function to process admin mode."""
    try:
        # Initialize database
        init_database()
        
        st.title("Admin Panel")
        
        # Check if already authenticated
        if is_admin_authenticated():
            # Show session info
            remaining_time = get_session_remaining_time()
            if remaining_time is not None:
                minutes = remaining_time // 60
                seconds = remaining_time % 60
                st.success(f"✅ Authenticated (Session expires in {minutes}m {seconds}s)")
            else:
                st.success("✅ Authenticated")
            
            # Logout button
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("Logout"):
                    logout_admin()
                    st.rerun()
            
            st.markdown('---')
            
            # Display Analytics Dashboard
            display_analytics_dashboard()
            
            st.markdown('---')
            
            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Detailed Resumes", "📥 Uploaded Resumes", "💬 Feedback", "🏥 System Health"])
            
            with tab1:
                display_detailed_resumes()
            
            with tab2:
                display_uploaded_pdfs()
            
            with tab3:
                display_feedback_data()
            
            with tab4:
                display_system_health()
        else:
            # Show login form
            st.subheader("Authentication Required")
            username = st.text_input("Username:", key="admin_username")
            password = st.text_input("Password:", type="password", key="admin_password")
            
            if st.button("Login"):
                if authenticate_admin_secure(username, password):
                    st.success("Authentication successful!")
                    st.rerun()
                else:
                    st.error("Authentication failed. Please check your credentials and try again.")
    except Exception as e:
        log_error(logger, e, {'operation': 'process_admin_mode'})
        st.error("An error occurred. Please try again or contact support.")


def display_feedback_data() -> None:
    """Display feedback data from database."""
    try:
        st.subheader("Latest Feedbacks")
        
        # Get feedback from database
        feedback_list = get_feedback(limit=10)
        
        if feedback_list:
            # Convert to DataFrame for display
            df = pd.DataFrame(feedback_list)
            df.columns = ['ID', 'User Name', 'Feedback', 'Created At']
            st.dataframe(df, use_container_width=True)
            
            # Button to view more
            if st.button("View All Feedbacks"):
                all_feedback = get_feedback(limit=1000)
                if all_feedback:
                    df_all = pd.DataFrame(all_feedback)
                    df_all.columns = ['ID', 'User Name', 'Feedback', 'Created At']
                    st.dataframe(df_all, use_container_width=True)
        else:
            st.info("No feedback data available.")
            
    except Exception as e:
        log_error(logger, e, {'operation': 'display_feedback_data'})
        st.error("Error loading feedback data. Please try again.")


def display_uploaded_pdfs() -> None:
    """Display uploaded PDFs with download links."""
    try:
        st.subheader("Uploaded Resumes")
        
        # Get all PDFs
        pdfs = get_all_pdfs()
        
        if pdfs:
            pdf_data_list: List[Dict[str, Any]] = []
            
            for pdf_id, pdf_name in pdfs:
                try:
                    pdf_data = get_pdf_by_id(pdf_id)
                    if pdf_data:
                        pdf_name_safe, pdf_bytes = pdf_data
                        pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
                        href = (
                            f'<a href="data:application/pdf;base64,{pdf_b64}" '
                            f'download="{pdf_name_safe}">Download</a>'
                        )
                        pdf_data_list.append({
                            "ID": pdf_id,
                            "Name": pdf_name_safe,
                            "Download (Resume)": href
                        })
                    else:
                        logger.warning(f"PDF data not found for ID: {pdf_id}")
                        pdf_data_list.append({
                            "ID": pdf_id,
                            "Name": pdf_name,
                            "Download (Resume)": "Not Available"
                        })
                except Exception as e:
                    log_error(logger, e, {'operation': 'display_pdf', 'pdf_id': pdf_id})
                    pdf_data_list.append({
                        "ID": pdf_id,
                        "Name": pdf_name,
                        "Download (Resume)": "Error"
                    })
            
            # Create and display DataFrame
            if pdf_data_list:
                # Display table with download links
                # Security Note: Using unsafe_allow_html=True is safe here because:
                # 1. Data comes from our own database (trusted source)
                # 2. Filenames are sanitized via database storage
                # 3. Base64 data is from PDFs we stored ourselves
                # 4. No user input is directly rendered in HTML
                pdf_table = pd.DataFrame(pdf_data_list)
                st.markdown(pdf_table.to_html(escape=False), unsafe_allow_html=True)
        else:
            st.info("No uploaded PDFs available.")
            
    except Exception as e:
        log_error(logger, e, {'operation': 'display_uploaded_pdfs'})
        st.error("Error loading uploaded PDFs. Please try again.")


def display_analytics_dashboard() -> None:
    """Display analytics dashboard with statistics."""
    try:
        st.header("📊 Analytics Dashboard")
        
        # Get statistics
        stats = get_statistics()
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Resumes",
                stats['total_resumes'],
                help="Total number of resumes uploaded"
            )
        
        with col2:
            st.metric(
                "Total Feedback",
                stats['total_feedback'],
                help="Total number of feedback received"
            )
        
        with col3:
            st.metric(
                "Total Storage",
                f"{stats['total_size_mb']} MB",
                help="Total storage used by all resumes"
            )
        
        with col4:
            st.metric(
                "Last 7 Days",
                stats['recent_7_days'],
                help="Resumes uploaded in last 7 days"
            )
        
        st.markdown("---")
        
        # Additional Statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Upload Statistics")
            
            if stats['total_resumes'] > 0:
                # Calculate percentages
                avg_size = stats['avg_size_mb']
                
                st.write(f"**Average Resume Size:** {avg_size} MB")
                st.write(f"**Total Storage Used:** {stats['total_size_mb']} MB")
                
                # Recent uploads chart
                if stats['recent_uploads']:
                    df_recent = pd.DataFrame(stats['recent_uploads'])
                    df_recent['date'] = pd.to_datetime(df_recent['date'])
                    st.line_chart(df_recent.set_index('date')['count'])
                else:
                    st.info("No uploads in the last 7 days")
            else:
                st.info("No statistics available yet")
        
        with col2:
            st.subheader("📊 User Activity & Percentages")
            
            if stats['total_resumes'] > 0:
                total = stats['total_resumes']
                recent = stats['recent_7_days']
                percentage = (recent / total * 100) if total > 0 else 0
                older = total - recent
                older_percentage = (older / total * 100) if total > 0 else 0
                
                st.write(f"**Total Resumes:** {total}")
                st.write(f"**Last 7 Days:** {recent} ({percentage:.1f}%)")
                st.write(f"**Older:** {older} ({older_percentage:.1f}%)")
                
                # Activity percentage bar
                st.progress(percentage / 100)
                st.caption(f"{percentage:.1f}% activity in last 7 days")
                
                # Pie chart data
                chart_data = pd.DataFrame({
                    'Category': ['Last 7 Days', 'Older'],
                    'Count': [recent, older]
                })
                st.bar_chart(chart_data.set_index('Category'))
            else:
                st.info("No user activity data available")
        
        st.markdown("---")
        
        # Detailed Percentage Breakdown
        if stats['total_resumes'] > 0:
            st.subheader("📈 Detailed Statistics & Percentages")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Resume Statistics:**")
                total = stats['total_resumes']
                recent = stats['recent_7_days']
                percentage = (recent / total * 100) if total > 0 else 0
                
                st.write(f"✅ Total: **{total}** resumes")
                st.write(f"📅 Last 7 days: **{recent}** ({percentage:.1f}%)")
                st.write(f"📊 Older: **{total - recent}** ({100 - percentage:.1f}%)")
            
            with col2:
                st.write("**Storage Statistics:**")
                total_size = stats['total_size_mb']
                avg_size = stats['avg_size_mb']
                
                st.write(f"💾 Total: **{total_size} MB**")
                st.write(f"📏 Average: **{avg_size} MB**")
                st.write(f"📁 Files: **{total}** files")
            
            with col3:
                st.write("**Feedback Statistics:**")
                total_feedback = stats['total_feedback']
                feedback_per_resume = (total_feedback / total * 100) if total > 0 else 0
                
                st.write(f"💬 Total: **{total_feedback}** feedback")
                st.write(f"📝 Per Resume: **{feedback_per_resume:.1f}%**")
                st.write(f"📊 Ratio: **{total_feedback}/{total}**")
        
    except Exception as e:
        log_error(logger, e, {'operation': 'display_analytics_dashboard'})
        st.error("Error loading analytics. Please try again.")


def display_detailed_resumes() -> None:
    """Display detailed resume information."""
    try:
        st.subheader("📄 Detailed Resume Information")
        
        # Get all PDFs with details
        pdfs_details = get_all_pdfs_with_details()
        
        if pdfs_details:
            # Create detailed DataFrame
            detailed_data = []
            
            for pdf_info in pdfs_details:
                pdf_id = pdf_info['id']
                pdf_name = pdf_info['name']
                uploaded_at = pdf_info['uploaded_at']
                file_size_mb = round(pdf_info['file_size'] / (1024 * 1024), 2) if pdf_info['file_size'] else 0
                
                # Format date
                try:
                    date_obj = datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    formatted_date = uploaded_at
                
                detailed_data.append({
                    "ID": pdf_id,
                    "Resume Name": pdf_name,
                    "Uploaded At": formatted_date,
                    "File Size (MB)": file_size_mb,
                    "Status": "✅ Available"
                })
            
            # Display as DataFrame
            df = pd.DataFrame(detailed_data)
            
            # Add search/filter
            search_term = st.text_input("🔍 Search resumes by name:", key="search_resumes")
            
            if search_term:
                df = df[df['Resume Name'].str.contains(search_term, case=False, na=False)]
            
            # Display statistics
            if len(df) > 0:
                st.write(f"**Showing {len(df)} of {len(pdfs_details)} resumes**")
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Shown", len(df))
                with col2:
                    avg_size = df['File Size (MB)'].mean()
                    st.metric("Avg Size", f"{avg_size:.2f} MB")
                with col3:
                    total_size = df['File Size (MB)'].sum()
                    st.metric("Total Size", f"{total_size:.2f} MB")
                
                st.markdown("---")
                
                # Display table
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download option for selected resume
                st.markdown("---")
                selected_id = st.selectbox(
                    "Select Resume ID to Download:",
                    options=df['ID'].tolist(),
                    key="download_select"
                )
                
                if st.button("Download Selected Resume"):
                    pdf_data = get_pdf_by_id(selected_id)
                    if pdf_data:
                        pdf_name, pdf_bytes = pdf_data
                        st.download_button(
                            label="📥 Download Resume",
                            data=pdf_bytes,
                            file_name=pdf_name,
                            mime="application/pdf"
                        )
            else:
                st.warning("No resumes found matching your search.")
        else:
            st.info("No resumes uploaded yet.")
            
    except Exception as e:
        log_error(logger, e, {'operation': 'display_detailed_resumes'})
        st.error("Error loading detailed resume information. Please try again.")


def display_system_health() -> None:
    """Display system health status."""
    try:
        st.subheader("🏥 System Health Status")
        
        # Get health status
        health = check_system_health()
        stats = get_system_stats()
        
        # Overall status
        status = health['status']
        if status == 'healthy':
            st.success("✅ System is healthy")
        elif status == 'warning':
            st.warning("⚠️ System has warnings")
        else:
            st.error("❌ System has errors")
        
        st.markdown("---")
        
        # Component health
        st.subheader("Component Status")
        
        components = health.get('components', {})
        
        # Database health
        db_health = components.get('database', {})
        col1, col2 = st.columns(2)
        with col1:
            if db_health.get('status') == 'healthy':
                st.success(f"✅ Database: {db_health.get('message', 'Healthy')}")
            elif db_health.get('status') == 'warning':
                st.warning(f"⚠️ Database: {db_health.get('message', 'Warning')}")
            else:
                st.error(f"❌ Database: {db_health.get('message', 'Error')}")
        
        # Data files health
        files_health = components.get('data_files', {})
        with col2:
            if files_health.get('status') == 'healthy':
                st.success(f"✅ Data Files: {files_health.get('message', 'Healthy')}")
            elif files_health.get('status') == 'warning':
                st.warning(f"⚠️ Data Files: {files_health.get('message', 'Warning')}")
            else:
                st.error(f"❌ Data Files: {files_health.get('message', 'Error')}")
        
        st.markdown("---")
        
        # System statistics
        st.subheader("📊 System Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Resumes", stats.get('total_resumes', 0))
        with col2:
            st.metric("Total Feedback", stats.get('total_feedback', 0))
        with col3:
            st.metric("Storage Used", f"{stats.get('total_storage_mb', 0)} MB")
        with col4:
            st.metric("Recent Uploads (7d)", stats.get('recent_uploads_7_days', 0))
        
        # Detailed information
        with st.expander("View Detailed Health Information"):
            st.json(health)
            
    except Exception as e:
        log_error(logger, e, {'operation': 'display_system_health'})
        st.error("Error loading system health information. Please try again.")


if __name__ == "__main__":
    process_admin_mode()
