import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table
from collections import Counter
import re

# Function to extract all skills from a column
def extract_all_skills(series):
    all_skills = []
    for item in series.dropna():
        skills = re.split(r',\s*|;\s*', item)
        all_skills.extend([skill.strip() for skill in skills])
    return all_skills

# Initialize the Dash app with custom CSS for Helvetica font
app = Dash(
    __name__, 
    suppress_callback_exceptions=True,
    external_stylesheets=[
        {
            'href': 'https://fonts.googleapis.com/css2?family=Helvetica&display=swap',
            'rel': 'stylesheet'
        }
    ]
)

# Define theme colors as specified
theme_colors = {
    'primary': '#296eb4',    # Primary blue 
    'secondary': '#ffe066',  # Yellow
    'white': '#ffffff',      # White
    'black': '#000000',      # Black
    'background': '#f8f9fa', # Light background
    'border': '#e0e0e0'      # Border color
}

# Add custom CSS for consistent font and color application
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                font-family: Helvetica, Arial, sans-serif !important;
            }
            .dash-header {
                color: ''' + theme_colors['primary'] + ''' !important;
            }
            .dash-tab {
                background-color: ''' + theme_colors['white'] + ''' !important;
                border-color: ''' + theme_colors['border'] + ''' !important;
            }
            .dash-tab--selected {
                border-top: 2px solid ''' + theme_colors['primary'] + ''' !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Read the cleaned Excel file
df = pd.read_excel("Regional Focussed Skill Training - Data (Cleaned).xlsx", sheet_name="Main")

# Get unique regions and skills
regions = df['Your Settlement/Location (Zone Wise)'].dropna().unique()
technical_skills = list(set(extract_all_skills(df['Which Skill would you like to learn?'])))
soft_skills = list(set(extract_all_skills(df['Which Soft Skill Would You like to learn?'])))
all_skills = list(set(extract_all_skills(df['Training Needs'])))

# App layout
app.layout = html.Div([
    html.H1("Regional Focused Skill Training Dashboard", 
             style={'textAlign': 'center', 
                    'color': theme_colors['primary'], 
                    'font-size': 40, 
                    'margin-top': '20px', 
                    'margin-bottom': '20px'}),
    
    # Horizontal filter bar at the top
    html.Div([
        html.H2("Filters", style={'margin-bottom': '15px', 'color': theme_colors['primary']}),
        
        html.Div([
            # First row of filters
            html.Div([
                html.Div([
                    html.P("Region:", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                    dcc.Dropdown(
                        id='region-selector',
                        options=[{'label': region, 'value': region} for region in regions] + [{'label': 'All Regions', 'value': 'all'}],
                        value='all',
                        style={'width': '100%'}
                    ),
                ], style={'width': '24%', 'display': 'inline-block', 'margin-right': '1%'}),
                
                html.Div([
                    html.P("Gender:", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                    dcc.Dropdown(
                        id='gender-selector',
                        options=[
                            {'label': 'All', 'value': 'all'},
                            {'label': 'Male', 'value': 'Male'},
                            {'label': 'Female', 'value': 'Female'}
                        ],
                        value='all',
                        style={'width': '100%'}
                    ),
                ], style={'width': '24%', 'display': 'inline-block', 'margin-right': '1%'}),
                
                html.Div([
                    html.P("Age Group:", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                    dcc.Dropdown(
                        id='age-selector',
                        options=[{'label': age, 'value': age} for age in df['Age Group'].dropna().unique()] + [{'label': 'All Ages', 'value': 'all'}],
                        value='all',
                        style={'width': '100%'}
                    ),
                ], style={'width': '24%', 'display': 'inline-block', 'margin-right': '1%'}),
                
                html.Div([
                    html.P("Skill Type:", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                    dcc.RadioItems(
                        id='skill-type-selector',
                        options=[
                            {'label': 'All Skills', 'value': 'all'},
                            {'label': 'Technical Skills', 'value': 'technical'},
                            {'label': 'Soft Skills', 'value': 'soft'}
                        ],
                        value='all',
                        inline=True,
                        style={'display': 'flex', 'justify-content': 'space-between'}
                    ),
                ], style={'width': '24%', 'display': 'inline-block'}),
            ], style={'display': 'flex', 'margin-bottom': '15px'}),
            
            # Second row - just for specific skill selector
            html.Div([
                html.P("Specific Skill (for detailed view):", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                dcc.Dropdown(
                    id='skill-selector',
                    options=[{'label': skill, 'value': skill} for skill in sorted(all_skills)],
                    value=all_skills[0] if all_skills else None,
                    style={'width': '100%'}
                ),
            ], style={'width': '100%', 'margin-bottom': '15px'})
        ], style={'padding': '15px', 
                   'background-color': theme_colors['background'], 
                   'border-radius': '10px', 
                   'margin-bottom': '20px', 
                   'border': f'1px solid {theme_colors["border"]}'})
    ]),
    
    # Main content area with tabs
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Overview', children=[
                html.Div([
                    html.Div([
                        html.H3("Demographics", style={'textAlign': 'center', 'color': theme_colors['primary']}),
                        dcc.Graph(id='gender-pie'),
                        dcc.Graph(id='region-pie')
                    ], style={'width': '48%', 'display': 'inline-block', 'margin-right': '2%', 'vertical-align': 'top'}),
                    
                    html.Div([
                        html.H3("Top Training Needs", style={'textAlign': 'center', 'color': theme_colors['primary']}),
                        dcc.Graph(id='top-skills-bar')
                    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'})
                ])
            ]),
            
            dcc.Tab(label='Regional Analysis', children=[
                html.Div([
                    html.Div([
                        html.H3("Regional Distribution of Selected Skill", style={'textAlign': 'center', 'color': theme_colors['primary']}),
                        dcc.Graph(id='regional-skill-bar')
                    ], style={'width': '100%', 'margin-bottom': '20px'}),
                    
                    html.Div([
                        html.H3("Top Skills by Region", style={'textAlign': 'center', 'color': theme_colors['primary']}),
                        dcc.Graph(id='regional-top-skills')
                    ], style={'width': '100%'})
                ])
            ]),
            
            dcc.Tab(label='Gender Analysis', children=[
                html.Div([
                    html.H3("Gender Comparison of Training Needs", style={'textAlign': 'center', 'color': theme_colors['primary']}),
                    dcc.Graph(id='gender-skills-comparison')
                ])
            ]),
            
            dcc.Tab(label='Trainee Details', children=[
                html.Div([
                    html.H3("Trainee Database", style={'textAlign': 'center', 'color': theme_colors['primary']}),
                    dash_table.DataTable(
                        id='trainee-table',
                        columns=[
                            {'name': 'Name', 'id': 'Name'},
                            {'name': 'Gender', 'id': 'Gender'},
                            {'name': 'Phone No.', 'id': 'Phone No.'},
                            {'name': 'Email', 'id': 'Email'},
                            {'name': 'Age Group', 'id': 'Age Group'},
                            {'name': 'Region', 'id': 'Your Settlement/Location (Zone Wise)'},
                            {'name': 'Education', 'id': 'Highest Education Qualification'},
                            {'name': 'Current Status', 'id': 'Current Status'},
                            {'name': 'Training Needs', 'id': 'Training Needs'}
                        ],
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'textAlign': 'left',
                            'padding': '10px',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'fontSize': '12px'
                        },
                        style_header={
                            'backgroundColor': theme_colors['primary'],
                            'color': theme_colors['white'],
                            'fontWeight': 'bold',
                            'fontSize': '14px'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': theme_colors['background']
                            },
                            {
                                'if': {'state': 'selected'},
                                'backgroundColor': f'{theme_colors["primary"]}20',  # Primary color with opacity
                                'border': f'1px solid {theme_colors["primary"]}'
                            }
                        ],
                        page_size=10,
                        filter_action="native",
                        sort_action="native"
                    )
                ])
            ])
        ], style={'font-size': '16px'}, colors={
            'border': theme_colors['border'],
            'primary': theme_colors['primary'],
            'background': theme_colors['background']
        })
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '20px'}),
    
    html.Div([
        html.Hr(),
        html.P("© 2025 Regional Focused Skill Training Dashboard. Created with Dash and Plotly.", 
               style={'textAlign': 'center', 'margin': '20px', 'color': theme_colors['primary']})
    ], style={'margin-top': '30px'})
])

# Define callback to update gender pie chart
@app.callback(
    Output('gender-pie', 'figure'),
    [Input('region-selector', 'value'),
     Input('age-selector', 'value')]
)
def update_gender_pie(selected_region, selected_age):
    filtered_df = df.copy()
    
    # Apply filters
    if selected_region != 'all':
        filtered_df = filtered_df[filtered_df['Your Settlement/Location (Zone Wise)'] == selected_region]
    
    if selected_age != 'all':
        filtered_df = filtered_df[filtered_df['Age Group'] == selected_age]
    
    # Check if there are any data after filtering
    if filtered_df.empty:
        return px.pie(title="No data available for the selected filters")
    
    # Create gender pie chart
    gender_counts = filtered_df['Gender'].value_counts()
    fig = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        title="Gender Distribution",
        color_discrete_sequence=[theme_colors['primary'], theme_colors['secondary'], '#A3C4BC']
    )
    
    fig.update_layout(
        legend=dict(orientation="h", y=-0.1),
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    
    return fig

# Define callback to update region pie chart
@app.callback(
    Output('region-pie', 'figure'),
    [Input('gender-selector', 'value'),
     Input('age-selector', 'value')]
)
def update_region_pie(selected_gender, selected_age):
    filtered_df = df.copy()
    
    # Apply filters
    if selected_gender != 'all':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    if selected_age != 'all':
        filtered_df = filtered_df[filtered_df['Age Group'] == selected_age]
    
    # Check if there are any data after filtering
    if filtered_df.empty:
        return px.pie(title="No data available for the selected filters")
    
    # Create region pie chart
    region_counts = filtered_df['Your Settlement/Location (Zone Wise)'].value_counts()
    fig = px.pie(
        names=region_counts.index,
        values=region_counts.values,
        title="Regional Distribution",
        color_discrete_sequence=[theme_colors['primary'], theme_colors['secondary'], '#A3C4BC', '#FFA07A', '#87CEFA', '#FFB6C1']
    )
    
    fig.update_layout(
        legend=dict(orientation="h", y=-0.1),
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    
    return fig

# Define callback to update top skills bar chart
@app.callback(
    Output('top-skills-bar', 'figure'),
    [Input('region-selector', 'value'),
     Input('gender-selector', 'value'),
     Input('age-selector', 'value'),
     Input('skill-type-selector', 'value')]
)
def update_top_skills_bar(selected_region, selected_gender, selected_age, skill_type):
    filtered_df = df.copy()
    
    # Apply filters
    if selected_region != 'all':
        filtered_df = filtered_df[filtered_df['Your Settlement/Location (Zone Wise)'] == selected_region]
    
    if selected_gender != 'all':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    if selected_age != 'all':
        filtered_df = filtered_df[filtered_df['Age Group'] == selected_age]
    
    # Check if there are any data after filtering
    if filtered_df.empty:
        return px.bar(title="No data available for the selected filters")
    
    # Extract skills based on selected skill type
    if skill_type == 'technical':
        skills = extract_all_skills(filtered_df['Which Skill would you like to learn?'])
        title = "Top Technical Skills"
    elif skill_type == 'soft':
        skills = extract_all_skills(filtered_df['Which Soft Skill Would You like to learn?'])
        title = "Top Soft Skills"
    else:
        skills = extract_all_skills(filtered_df['Training Needs'])
        title = "Top Overall Training Needs"
    
    # Count skills and get top 10 (or fewer if there aren't 10)
    skill_counts = Counter(skills)
    
    # Check if there are any skills after filtering
    if not skill_counts:
        return px.bar(title=f"No {title.lower()} available for the selected filters")
    
    top_skills = pd.DataFrame(skill_counts.most_common(10), columns=['Skill', 'Count'])
    
    # Create bar chart
    fig = px.bar(
        top_skills,
        x='Count',
        y='Skill',
        orientation='h',
        title=title,
        color='Count',
        color_continuous_scale=[[0, theme_colors['primary']], [1, theme_colors['secondary']]]
    )
    
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=20, r=20, t=40, b=20),
        height=600
    )
    
    return fig

# Define callback to update regional skill bar chart
@app.callback(
    Output('regional-skill-bar', 'figure'),
    [Input('skill-selector', 'value'),
     Input('gender-selector', 'value'),
     Input('age-selector', 'value')]
)
def update_regional_skill_bar(selected_skill, selected_gender, selected_age):
    filtered_df = df.copy()
    
    # Apply filters
    if selected_gender != 'all':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    if selected_age != 'all':
        filtered_df = filtered_df[filtered_df['Age Group'] == selected_age]
    
    # Check if there are any data after filtering
    if filtered_df.empty:
        return px.bar(title="No data available for the selected filters")
    
    # Check if a skill is selected
    if not selected_skill:
        return px.bar(title="Please select a skill to view its regional distribution")
    
    # Calculate regional distribution for selected skill
    region_data = []
    
    for region in regions:
        region_df = filtered_df[filtered_df['Your Settlement/Location (Zone Wise)'] == region]
        region_total = len(region_df)
        
        if region_total > 0:
            region_skills = extract_all_skills(region_df['Training Needs'])
            skill_count = sum(1 for skill in region_skills if skill == selected_skill)
            skill_percent = (skill_count / region_total) * 100
            
            region_data.append({
                'Region': region,
                'Count': skill_count,
                'Percentage': skill_percent,
                'Total Respondents': region_total
            })
    
    # Check if there's any data for the selected skill
    if not region_data:
        return px.bar(title=f"No data for '{selected_skill}' in any region")
    
    region_data_df = pd.DataFrame(region_data)
    
    # Create bar chart
    fig = px.bar(
        region_data_df,
        x='Region',
        y='Percentage',
        title=f"Regional Distribution of '{selected_skill}'",
        text='Count',
        color='Percentage',
        color_continuous_scale=[[0, theme_colors['primary']], [1, theme_colors['secondary']]],
        hover_data=['Total Respondents']
    )
    
    fig.update_layout(
        xaxis_title="Region",
        yaxis_title="Percentage of Regional Respondents",
        margin=dict(l=20, r=20, t=40, b=20),
        height=400
    )
    
    return fig

# Define callback to update regional top skills
@app.callback(
    Output('regional-top-skills', 'figure'),
    [Input('region-selector', 'value'),
     Input('gender-selector', 'value'),
     Input('age-selector', 'value'),
     Input('skill-type-selector', 'value')]
)
def update_regional_top_skills(selected_region, selected_gender, selected_age, skill_type):
    filtered_df = df.copy()
    
    # Apply gender and age filters
    if selected_gender != 'all':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    if selected_age != 'all':
        filtered_df = filtered_df[filtered_df['Age Group'] == selected_age]
    
    # Check if there are any data after filtering
    if filtered_df.empty:
        return px.bar(title="No data available for the selected filters")
    
    # Decide which regions to include
    if selected_region != 'all':
        regions_to_include = [selected_region]
    else:
        # Only include regions with more than 3 respondents
        regions_to_include = [region for region in regions 
                            if len(filtered_df[filtered_df['Your Settlement/Location (Zone Wise)'] == region]) > 3]
    
    # Check if there are any regions to analyze
    if not regions_to_include:
        return px.bar(title="No regions with enough respondents for the selected filters")
    
    # Prepare data for chart
    chart_data = []
    
    for region in regions_to_include:
        region_df = filtered_df[filtered_df['Your Settlement/Location (Zone Wise)'] == region]
        region_total = len(region_df)
        
        if region_total == 0:
            continue
        
        # Extract skills based on selected skill type
        if skill_type == 'technical':
            region_skills = extract_all_skills(region_df['Which Skill would you like to learn?'])
            if not region_skills:
                continue
        elif skill_type == 'soft':
            region_skills = extract_all_skills(region_df['Which Soft Skill Would You like to learn?'])
            if not region_skills:
                continue
        else:
            region_skills = extract_all_skills(region_df['Training Needs'])
            if not region_skills:
                continue
        
        # Get top 5 skills for this region
        skill_counts = Counter(region_skills)
        if not skill_counts:
            continue
            
        top_skills = skill_counts.most_common(5)
        
        for skill, count in top_skills:
            percentage = (count / region_total) * 100
            chart_data.append({
                'Region': region,
                'Skill': skill,
                'Count': count,
                'Percentage': percentage,
                'Total Respondents': region_total
            })
    
    # Check if there's any data to display
    if not chart_data:
        return px.bar(title=f"No data available for the selected skill type and filters")
    
    chart_df = pd.DataFrame(chart_data)
    
    # Create grouped bar chart
    fig = px.bar(
        chart_df,
        x='Region',
        y='Percentage',
        color='Skill',
        barmode='group',
        title="Top 5 Skills by Region",
        text='Count',
        hover_data=['Total Respondents'],
        color_discrete_sequence=[theme_colors['primary'], theme_colors['secondary'], '#A3C4BC', '#FFA07A', '#87CEFA']
    )
    
    fig.update_layout(
        xaxis_title="Region",
        yaxis_title="Percentage of Regional Respondents",
        legend_title="Skill",
        margin=dict(l=20, r=20, t=40, b=20),
        height=500
    )
    
    return fig

# Define callback to update gender skills comparison
@app.callback(
    Output('gender-skills-comparison', 'figure'),
    [Input('region-selector', 'value'),
     Input('age-selector', 'value'),
     Input('skill-type-selector', 'value')]
)
def update_gender_skills_comparison(selected_region, selected_age, skill_type):
    filtered_df = df.copy()
    
    # Apply filters
    if selected_region != 'all':
        filtered_df = filtered_df[filtered_df['Your Settlement/Location (Zone Wise)'] == selected_region]
    
    if selected_age != 'all':
        filtered_df = filtered_df[filtered_df['Age Group'] == selected_age]
    
    # Check if there are any data after filtering
    if filtered_df.empty:
        return px.bar(title="No data available for the selected filters")
    
    # Split by gender
    male_df = filtered_df[filtered_df['Gender'] == 'Male']
    female_df = filtered_df[filtered_df['Gender'] == 'Female']
    
    # Check if there are data for both genders
    if male_df.empty or female_df.empty:
        return px.bar(title="Insufficient data for gender comparison with the selected filters")
    
    # Extract skills based on selected skill type
    if skill_type == 'technical':
        male_skills = extract_all_skills(male_df['Which Skill would you like to learn?'])
        female_skills = extract_all_skills(female_df['Which Skill would you like to learn?'])
        title = "Gender Comparison of Technical Skills"
    elif skill_type == 'soft':
        male_skills = extract_all_skills(male_df['Which Soft Skill Would You like to learn?'])
        female_skills = extract_all_skills(female_df['Which Soft Skill Would You like to learn?'])
        title = "Gender Comparison of Soft Skills"
    else:
        male_skills = extract_all_skills(male_df['Training Needs'])
        female_skills = extract_all_skills(female_df['Training Needs'])
        title = "Gender Comparison of Overall Training Needs"
    
    # Check if there are skills for both genders
    if not male_skills or not female_skills:
        return px.bar(title=f"Insufficient {skill_type} skills data for gender comparison")
    
    # Get top skills for each gender
    male_counts = Counter(male_skills)
    female_counts = Counter(female_skills)
    
    # Get the top 7 skills overall to compare
    all_skills = male_skills + female_skills
    all_skills_counter = Counter(all_skills)
    
    # Check if there are any skills to display
    if not all_skills_counter:
        return px.bar(title=f"No skills data available for the selected filters")
    
    top_skills = [skill for skill, _ in all_skills_counter.most_common(7)]
    
    # Calculate percentages
    chart_data = []
    
    for skill in top_skills:
        male_count = male_counts.get(skill, 0)
        female_count = female_counts.get(skill, 0)
        
        male_pct = (male_count / len(male_df)) * 100 if len(male_df) > 0 else 0
        female_pct = (female_count / len(female_df)) * 100 if len(female_df) > 0 else 0
        
        chart_data.append({
            'Skill': skill,
            'Gender': 'Male',
            'Percentage': male_pct,
            'Count': male_count
        })
        
        chart_data.append({
            'Skill': skill,
            'Gender': 'Female',
            'Percentage': female_pct,
            'Count': female_count
        })
    
    chart_df = pd.DataFrame(chart_data)
    
    # Create grouped bar chart
    fig = px.bar(
        chart_df,
        x='Skill',
        y='Percentage',
        color='Gender',
        barmode='group',
        title=title,
        text='Count',
        color_discrete_sequence=[theme_colors['primary'], theme_colors['secondary']]  # Blue for male, yellow for female
    )
    
    fig.update_layout(
        xaxis_title="Skill",
        yaxis_title="Percentage of Gender Group",
        legend_title="Gender",
        margin=dict(l=20, r=20, t=40, b=20),
        height=500,
        xaxis={'tickangle': -45}  # Angle the x-axis labels for better readability
    )
    
    return fig

# Define callback to update trainee table
@app.callback(
    Output('trainee-table', 'data'),
    [Input('region-selector', 'value'),
     Input('gender-selector', 'value'),
     Input('age-selector', 'value'),
     Input('skill-selector', 'value')]
)
def update_trainee_table(selected_region, selected_gender, selected_age, selected_skill):
    filtered_df = df.copy()
    
    # Apply filters
    if selected_region != 'all':
        filtered_df = filtered_df[filtered_df['Your Settlement/Location (Zone Wise)'] == selected_region]
    
    if selected_gender != 'all':
        filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
    
    if selected_age != 'all':
        filtered_df = filtered_df[filtered_df['Age Group'] == selected_age]
    
    # Filter by selected skill if applicable
    if selected_skill:
        # We need to find trainees who have the selected skill in their training needs
        skill_matches = []
        
        for idx, row in filtered_df.iterrows():
            training_needs = row['Training Needs']
            if pd.isna(training_needs):
                continue
                
            skills = [skill.strip() for skill in re.split(r',\s*|;\s*', training_needs)]
            if selected_skill in skills:
                skill_matches.append(idx)
        
        filtered_df = filtered_df.loc[skill_matches] if skill_matches else pd.DataFrame(columns=filtered_df.columns)
    
    # Return data for table
    return filtered_df.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)