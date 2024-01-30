import streamlit as st
import pandas as pd
import plotly.express as px
import time
import plotly.graph_objects as go



# Set page title and layout
st.set_page_config(page_title='Shaping Sustainable Future', page_icon=':earth_africa:',layout='wide')

holiday_energy_acorn = pd.read_csv('holiday_energy_acorn.csv')
weather = pd.read_csv('holiday_energy_acorn_weather.csv')

#changing datatype
holiday_energy_acorn['time'] = pd.to_datetime(holiday_energy_acorn['time'])
holiday_energy_acorn['energy(kWh/hh)'] = pd.to_numeric(holiday_energy_acorn['energy(kWh/hh)'])

# Sidebar
st.sidebar.title('Navigation')
section = st.sidebar.radio('Go to', ('Acorn_grouped Energy Consumption', 'Problem Description', 'Weather data'))

# st.sidebar.title('Filter Data')
# filter_option = st.sidebar.selectbox('Filter Option', ('All Data', 'By Month and Year'))

#title
st.markdown(
    """
    <div style="text-align: center;">
        <h1>
            &#x1F4A1; &#x1F3E0; SHAPING A SUSTAINABLE FUTURE &#x2601;&#xFE0F; &#x2600;&#xFE0F;
            <h3><i>Analyzing Energy Consumption in London Homes with Smart Meter Data and Weather Insights<i></h3>
        </h1>
        <hr style="border: 0.5px solid #888; margin: 30px auto; width: 50%;">
    </div>    """,
    unsafe_allow_html=True
)


# Data Summary section
if section == 'Acorn_grouped Energy Consumption':
    st.title(':small_orange_diamond: Data Summary')
    st.write('This section provides a summary of the dataset.')

    # Display dataset summary
#     st.subheader('Dataset Overview')
#     st.write(data.head())

    # Display dataset statistics
#     st.subheader('Dataset Statistics')
#     st.write(data.describe())

    # Display data visualization (example: interactive histogram using Plotly)
    st.subheader('Data Visualization')

    # Suppress the FutureWarning
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
#-------------------------------------------------------------------------------
    with st.spinner('Loading Visualizations...'):
        # Default plot with all the data
        #         if filter_option == 'All Data':


        # grouped_data = holiday_energy_acorn.groupby(['Acorn_grouped', 'stdorToU'])['energy(kWh/hh)'].mean().reset_index()

        # # Create a grouped bar chart
        # fig = px.bar(holiday_energy_acorn, x='Acorn_grouped', y='energy(kWh/hh)', color='stdorToU',
        #             title='Energy Consumption by Acorn Grouped and stdorToU',
        #             labels={'Acorn_grouped': 'Acorn Grouped', 'energy(kWh/hh)': 'Total Energy Consumption (kWh/hh)'},
        #             facet_col='stdorToU')

        # Display the chart
        # st.plotly_chart(fig)
        col1, col2 = st.columns([2.1,1.5])
        with col1:
            unique_Acorn_grouped = holiday_energy_acorn['Acorn_grouped'].unique()

            # Dropdown menu for choosing LCLid
            selected_Acorn_grouped = st.sidebar.selectbox('Select Acorn_grouped', unique_Acorn_grouped, format_func=lambda x: x)

            # Filter data based on selected LCLid
            filtered_data = holiday_energy_acorn[holiday_energy_acorn['Acorn_grouped'] == selected_Acorn_grouped]

            # Line plot
            fig = px.line(filtered_data, x='time', y='energy(kWh/hh)', title=f'Energy Consumption for Acorn_grouped: {selected_Acorn_grouped}')
            st.plotly_chart(fig)
            
            holiday_energy_acorn = filtered_data
        with col2:
            # Calculate the average energy consumption per year
            yearly_avg = holiday_energy_acorn.groupby(holiday_energy_acorn['time'].dt.to_period('Y'))['energy(kWh/hh)'].mean().reset_index()
            yearly_avg['time'] = yearly_avg['time'].astype(str)

            # Create a line plot for yearly average energy consumption
            fig_yearly = px.bar(yearly_avg, x='time', y='energy(kWh/hh)', title='Average Energy Consumption by Year')

            # Customize the layout to adjust the size of the figure
            fig_yearly.update_layout(
                width=400,  # Set the width of the figure
                height=450,  # Set the height of the figure
            )
            st.plotly_chart(fig_yearly)

        # Add a slider for selecting a specific year
        min_year = holiday_energy_acorn['time'].dt.year.min()
        max_year = holiday_energy_acorn['time'].dt.year.max()
        if min_year == max_year:
            selected_year = min_year
        else:
            selected_year = st.slider('Select a Year', min_value=min_year, max_value=max_year)

        selected_year_data = holiday_energy_acorn[holiday_energy_acorn['time'].dt.year == selected_year]

        # Calculate the mean, sum, highest, and lowest energy consumption
#             mean_energy = hh_energy_acorn['energy(kWh/hh)'].mean()
#             sum_energy = hh_energy_acorn['energy(kWh/hh)'].sum()
        highest_energy = selected_year_data['energy(kWh/hh)'].max()
        lowest_energy = selected_year_data['energy(kWh/hh)'].min()

        # Find the corresponding Acorn and stdorToU values for the highest energy consumption
        highest_energy_row = selected_year_data[holiday_energy_acorn['energy(kWh/hh)'] == highest_energy].iloc[0]
        highest_date = highest_energy_row['time']
        highest_acorn = highest_energy_row['Acorn']
        highest_stdorToU = highest_energy_row['stdorToU']

        # Find the corresponding Acorn and stdorToU values for the lowest energy consumption
        lowest_energy_row = selected_year_data[holiday_energy_acorn['energy(kWh/hh)'] == lowest_energy].iloc[0]
        lowest_date = lowest_energy_row['time']
        lowest_acorn = lowest_energy_row['Acorn']
        lowest_stdorToU = lowest_energy_row['stdorToU']

        # Search for the date with the maximum energy in the holiday dataset
        holiday_date_h = holiday_energy_acorn[holiday_energy_acorn['time'].dt.date == highest_date.date()]

        # Search for the date with the minimum energy in the holiday dataset
        holiday_date_l = holiday_energy_acorn[holiday_energy_acorn['time'].dt.date == lowest_date.date()]

        # Display the statistics
#             st.subheader('Energy Consumption Statistics (All Data)')
#             st.write('**Mean Energy Consumption:**', mean_energy)
#             st.write('**Sum Energy Consumption:**', sum_energy)
#             st.markdown('<hr>', unsafe_allow_html=True)


        col1, col2 = st.columns(2)
        with col1:
            st.subheader(':exclamation: Highest Energy Consumption')

            st.write('**Energy:**', highest_energy)
            st.write('**Date:**', highest_date)
            st.write('**Acorn:**', highest_acorn)
            st.write('**stdorToU:**', highest_stdorToU)
            # Check if a holiday was found for the date
            if holiday_date_h.isna().any().any():
                holiday = 'No holiday'
            else:
                holiday = holiday_date_h['Type'].values[0]
            st.write('**Holiday:**', holiday)

        with col2:
            st.subheader('Lowest Energy Consumption')

            st.write('**Energy:**', lowest_energy)
            st.write('**Date:**', lowest_date)
            st.write('**Acorn:**', lowest_acorn)
            st.write('**stdorToU:**', lowest_stdorToU)
            # Check if a holiday was found for the date
            if holiday_date_l.isna().any().any():
                holiday = 'No holiday'
            else:
                holiday = holiday_date_l['Type'].values[0]
            st.write('**Holiday:**', holiday)


        # Calculate the average energy consumption per weekday
        holiday_energy_acorn['weekday'] = holiday_energy_acorn['time'].dt.day_name()
        weekday_avg = holiday_energy_acorn.groupby('weekday')['energy(kWh/hh)'].mean().reset_index()


        # Define the desired order of weekdays
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Convert the 'weekday' column to a categorical variable with the desired order
        weekday_avg['weekday'] = pd.Categorical(weekday_avg['weekday'], categories=weekday_order, ordered=True)

        # Sort the dataframe by the ordered 'weekday' column
        weekday_avg = weekday_avg.sort_values('weekday')

        # Create a line plot using Plotly Express
        fig = px.line(weekday_avg, x='weekday', y='energy(kWh/hh)', title='Average Energy Consumption by Weekday')

        # Render the plot using Streamlit
        st.plotly_chart(fig)

        with col1:
            # Calculate the average energy consumption per month
            monthly_avg = holiday_energy_acorn.groupby(holiday_energy_acorn['time'].dt.to_period('M'))['energy(kWh/hh)'].mean().reset_index()
            monthly_avg['time'] = monthly_avg['time'].astype(str)  # Convert Period to string

            # Create a line plot for monthly average energy consumption
            fig_monthly = px.line(monthly_avg, x='time', y='energy(kWh/hh)', title='Average Energy Consumption by Month')


            # Render the plots using Streamlit
            st.plotly_chart(fig_monthly)

        with col2:
            # Group the data by holiday and calculate the total energy consumption for each holiday
            holiday_energy_acorn = holiday_energy_acorn.groupby(['Type', 'time'])['energy(kWh/hh)'].sum().reset_index()

            # Create a pie chart showing energy consumption by holiday
            fig_holidays = px.pie(holiday_energy_acorn, values='energy(kWh/hh)', names='Type', title='Energy Consumption by Holiday')

            fig_holidays.update_traces(hovertemplate='Type: %{label}<br>Energy: %{value:.2f} kWh<br>Date: %{text}', text=holiday_energy_acorn['time'], textinfo='percent')


            fig_holidays.update_layout(showlegend=False)

            # Render the plot using Streamlit
            st.plotly_chart(fig_holidays)

#-------------------------------------------------------------------------------
elif section == 'Weather data':
    st.title('Energy Consumption Visualizations')

    # Raw data
    st.subheader('Raw data')
    st.dataframe(weather)

    # # Time Series Plot
    # st.subheader('Energy Consumption Over Time')
    # weather['time'] = pd.to_datetime(weather['time'])
    # fig = px.line(weather, x='time', y='energy(kWh/hh)')
    # st.plotly_chart(fig)

    # # Scatter Plot - Temperature, Pressure, and Energy Consumption
    # st.subheader('Temperature, Pressure, and Energy Consumption')
    # fig = px.scatter_3d(weather, x='temperature', y='pressure', z='energy(kWh/hh)',
    #                     color='energy(kWh/hh)', size_max=5)
    # fig.update_layout(scene=dict(xaxis_title='Temperature',
    #                             yaxis_title='Pressure',
    #                             zaxis_title='Energy Consumption (kWh/hh)'))
    # st.plotly_chart(fig)

    # # Scatter Plot
    # st.subheader('Energy Consumption vs Temperature')
    # fig = px.scatter(weather, x='temperature', y='energy(kWh/hh)')
    # st.plotly_chart(fig)

    # # Histogram
    # st.subheader('Distribution of Energy Consumption')
    # fig = px.histogram(weather, x='energy(kWh/hh)', nbins=20)
    # st.plotly_chart(fig)

    # # Pie Chart
    # st.subheader('Customer Distribution by Acorn Group')
    # grouped_customers = weather['Acorn_grouped'].value_counts().reset_index()
    # grouped_customers.columns = ['Acorn_grouped', 'Count']
    # fig = px.pie(grouped_customers, values='Count', names='Acorn_grouped')
    # st.plotly_chart(fig)


            
       
                

    
#-------------------------------------------------------------------------------    
# Problem Description section
elif section == 'Problem Description':
    st.title(':small_orange_diamond: Problem Description')
    st.write('This section describes the problem at hand and any relevant details.')

    # Add problem description content here

# Footer
st.sidebar.markdown('---')
st.sidebar.text("Done With \u2764\ufe0f By Maryam")
