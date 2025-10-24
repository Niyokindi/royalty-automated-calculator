"""
Streamlit App for Music Royalty Automation
Upload contracts and royalty statements to calculate and visualize payments

Installation:
pip install streamlit plotly pandas

Usage:
streamlit run streamlit_app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import tempfile
import os
from pathlib import Path

# Import your existing modules from the parser package
from parser import RoyaltyCalculator

# Page configuration
st.set_page_config(
    page_title="Music Royalty Automation",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    h1 {
        color: #1DB954;
        padding-bottom: 1rem;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


def save_uploaded_file(uploaded_file):
    """Save uploaded file to temporary directory and return path"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None


def create_pie_chart(payments):
    """Create an interactive pie chart for royalty splits"""
    if not payments:
        return None
    
    # Aggregate by party across all songs
    party_totals = {}
    party_details = {}  # Store breakdown by song
    
    for payment in payments:
        # Sum total amounts
        if payment.party_name not in party_totals:
            party_totals[payment.party_name] = 0
            party_details[payment.party_name] = []
        
        party_totals[payment.party_name] += payment.amount_to_pay
        
        # Store details for hover
        party_details[payment.party_name].append({
            'song': payment.song_title,
            'percentage': payment.percentage,
            'amount': payment.amount_to_pay,
            'type': payment.royalty_type
        })
    
    # Create lists for the pie chart
    parties = []
    amounts = []
    display_texts = []
    hover_texts = []
    
    for party, total_amount in party_totals.items():
        parties.append(party)
        amounts.append(total_amount)
        
        # Build detailed hover text
        details = party_details[party]
        hover_lines = [f"<b>{party}</b>", f"Total: ${total_amount:,.2f}", ""]
        
        # Group by song
        songs = {}
        for detail in details:
            song = detail['song']
            if song not in songs:
                songs[song] = []
            songs[song].append(detail)
        
        # Add song breakdown
        for song, song_details in songs.items():
            hover_lines.append(f"<b>{song}:</b>")
            for detail in song_details:
                hover_lines.append(f"  • {detail['percentage']}% ({detail['type']}): ${detail['amount']:,.2f}")
        
        hover_texts.append("<br>".join(hover_lines))
        display_texts.append(f"{party}<br>${total_amount:,.2f}")
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=parties,
        values=amounts,
        text = display_texts,
        # textinfo='label+value',
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover_texts,
        marker=dict(
            colors=px.colors.qualitative.Set3,
            line=dict(color='white', width=2)
        )
    )])
    
    fig.update_layout(
        showlegend=True,
        height=500,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )
    
    return fig


def create_payment_table(payments):
    """Create a detailed payment breakdown table"""
    if not payments:
        return None
    
    data = []
    for payment in payments:
        data.append({
            "Work": payment.song_title,
            "Payee": payment.party_name,
            "Role": payment.role,
            "Type": payment.royalty_type.title(),
            "Total Royalty": f"${payment.total_royalty:,.2f}",
            "Share %": f"{payment.percentage}%",
            "Amount to Pay": f"${payment.amount_to_pay:,.2f}"
        })
    
    df = pd.DataFrame(data)
    return df


def create_summary_metrics(payments):
    """Create summary metric cards"""
    if not payments:
        return None
    
    total_amount = sum(p.amount_to_pay for p in payments)
    unique_payees = len(set(p.party_name for p in payments))
    unique_songs = len(set(p.song_title for p in payments))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="💰 Total Payout",
            value=f"${total_amount:,.2f}"
        )
    
    with col2:
        st.metric(
            label="👥 Contributors",
            value=unique_payees
        )
    
    with col3:
        st.metric(
            label="🎵 Songs",
            value=unique_songs
        )


def main():
    # Header
    st.title("🎵 Music Royalty Automation System")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. **Upload Contract** (PDF or Excel)
        2. **Upload Royalty Statement** (Excel)
        3. **Click 'Calculate Payments'**
        4. **View Results & Download**
        """)
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Upload Contract")
        contract_files = st.file_uploader(
            "Upload contract(s) file",
            type=['pdf', 'xlsx', 'xls'],
            help="Upload the music contract (PDF or Excel format)",
            accept_multiple_files = True
        )
        
        if contract_files:
            for file in contract_files:
                st.success(f"{file.name} uploaded")
    
    with col2:
        st.subheader("📊 Upload Royalty Statement")
        statement_file = st.file_uploader(
            "Upload royalty statement",
            type=['xlsx', 'xls'],
            help="Upload the Excel royalty statement from your distributor"
        )
        
        if statement_file:
            st.success(f"{statement_file.name} uploaded successfully")
    
    st.markdown("---")
    
    # Calculate button
    if contract_files and statement_file:
        if st.button("Calculate Payments", type="primary", use_container_width=True):
            with st.spinner("Processing files... This may take a moment."):
                try:
                    # Save uploaded statement
                    statement_path = save_uploaded_file(statement_file)
                    if not statement_path:
                        st.error("Failed to process royalty statement")
                        st.stop()

                    # Save all contract files
                    contract_paths = []
                    for contract_file in contract_files:
                        path = save_uploaded_file(contract_file)
                        if path:
                            contract_paths.append(path)

                    if not contract_paths:
                        st.error("No valid contract files were processed")
                        st.stop()

                    # Initialize calculator
                    calculator = RoyaltyCalculator()

                    # New method that handles multiple contracts
                    payments = calculator.calculate_payments_from_contracts(contract_paths, statement_path)

                    # Store results in session state
                    st.session_state["payments"] = payments
                    st.session_state["calculator"] = calculator

                    # Clean up temp files
                    for path in contract_paths:
                        os.unlink(path)
                    os.unlink(statement_path)

                    st.success(f"✅ Processed {len(contract_paths)} contracts and calculated payments successfully!")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.exception(e)
    
    # Display results if available
    if 'payments' in st.session_state and st.session_state['payments']:
        payments = st.session_state['payments']
        calculator = st.session_state['calculator']
        
        st.markdown("---")
        st.header("Results")
        
        # Summary metrics
        create_summary_metrics(payments)
        
        st.markdown("---")
        
        # Visualization and table in columns
        viz_col, table_col = st.columns([1, 1])
        
        with viz_col:
            st.subheader("Payment Distribution")
            fig = create_pie_chart(payments)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with table_col:
            st.subheader("Payment Breakdown")
            df = create_payment_table(payments)
            if df is not None:
                st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Detailed breakdown by party
        st.subheader("Detailed Breakdown by Contributor")
        
        # Group payments by party
        party_groups = {}
        for payment in payments:
            if payment.party_name not in party_groups:
                party_groups[payment.party_name] = []
            party_groups[payment.party_name].append(payment)
        
        for party_name, party_payments in party_groups.items():
            with st.expander(f"{party_name} - Total: ${sum(p.amount_to_pay for p in party_payments):,.2f}"):
                for payment in party_payments:
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        st.write(f"**{payment.song_title}**")
                    with col2:
                        st.write(f"*{payment.royalty_type.title()}*")
                    with col3:
                        st.write(f"`{payment.percentage}%`")
                    with col4:
                        st.write(f"**${payment.amount_to_pay:,.2f}**")
        
        st.markdown("---")
        
       # Export to Excel
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                calculator.save_payments_to_excel(payments, tmp_file.name)
                
                with open(tmp_file.name, 'rb') as f:
                    st.download_button(
                        label="💾 Download Excel Report File",
                        data=f.read(),
                        file_name="royalty_payments.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                os.unlink(tmp_file.name)
        except Exception as e:
            st.error(f"Error creating Excel file: {str(e)}")
    
    elif contract_files and statement_file:
        st.info("Click 'Calculate Payments' to process your files")
    else:
        st.info("Please upload both contract and royalty statement files to begin")


if __name__ == "__main__":
    main()