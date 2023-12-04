from dash import html, dcc, dash_table, Output, Input, State
import dash_bootstrap_components as dbc
import dash
from shapash.utils.load_smartpredictor import load_smartpredictor
import math
import pandas as pd
import plotly.express as px
import base64
from wordcloud import WordCloud
import matplotlib.pyplot as plt

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY], title='ML Projects')

server = app.server

img = "faces1.jpeg"
img1 = "faces2.jpeg"
img2 = "face3.jpeg"
img3 = "face4.jpeg"
img4 = "faces9.jpeg"
img5 = "face6.jpeg"
img6 = "faces5.jpeg"
img7 = "faces7.jpeg"
img8 = "faces8.jpeg"
img9 = "faces10.jpeg"
img10 = "DEM.jpg"


def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


app.layout = dbc.Container([
    dbc.Row(
        [
            dbc.Row([
                dbc.Col(dbc.CardBody(html.Img(src=b64_image(img10), width=64, height=64)),
                        style={'alignItems': 'center', 'justifyContent': 'center'}, md=4, sm=12, lg=4),
            ]),
            dbc.Row([
                html.P(['Diagnose Explain and Match(DEM Model)'],
                       style={'marginBottom': 15, 'text-align': 'center', 'color': 'Green',
                              'fontSize': 24})
            ], justify="center"),
            dbc.Col([

                html.P(['Have you experience the following Symptoms?'],
                       style={'marginBottom': 15, 'marginTop': 5, 'color': 'Green', 'fontSize': 14}),
                dcc.Dropdown(['itching', 'skinrash', 'nodal skin eruptions', 'weight loss'
                              ], multi=False, placeholder="symptoms",
                             clearable=True, optionHeight=50, value='skinrash',
                             style={'color': '#F71AF7', 'fontSize': 14}, id="drp"),

                html.P(['Are you experiencing this symptoms at the moment?'],
                       style={'marginBottom': 15, 'marginTop': 5, 'color': 'Green', 'fontSize': 14}),
                dcc.Dropdown(['continuous sneezing', 'restlessness',
                              'shivering', 'chills',
                              ], multi=False, placeholder="symptoms",
                             clearable=True, optionHeight=50, value='chills',
                             style={'color': 'LimeGreen', 'fontSize': 14}, id="drp1"),

                html.P(['Are these symptoms common to you Right now?'],
                       style={'marginBottom': 15, 'marginTop': 5, 'color': 'Green', 'fontSize': 14}),
                dcc.Dropdown(['joint pain', 'stomach pain', 'acidity', 'small dents in nails'
                              ], multi=False, placeholder="symptoms",
                             clearable=True, optionHeight=50, value='acidity',
                             style={'color': '#0EE3D1', 'fontSize': 14}, id="drp2"),

                html.P(['Are these symptoms relateable?'],
                       style={'marginBottom': 15, 'marginTop': 5, 'color': 'Green', 'fontSize': 14}),
                dcc.Dropdown(['ulcers on tongue', 'muscle wasting', 'vomiting', 'lethargy'
                              ], multi=False, placeholder="symptoms",
                             clearable=True, optionHeight=50, value='vomiting',
                             style={'color': '#FF11F1', 'fontSize': 14}, id="drp3"),

                html.P(['Are you experiencing this symptoms at the moment'],
                       style={'marginBottom': 15, 'marginTop': 5, 'color': 'Green', 'fontSize': 14}),
                dcc.Dropdown(['burning micturition', 'inflammatory nails', 'blister'
                              ], multi=False, placeholder="symptoms",
                             clearable=True, optionHeight=50, value='blister',
                             style={'color': '#F40C0F', 'fontSize': 14}, id="drp4"),

                html.P(['Are you experiencing the following symptoms'],
                       style={'marginBottom': 15, 'marginTop': 5, 'color': 'Green', 'fontSize': 14}),
                dcc.Dropdown(['cold hands and feets', 'mood swings', 'weight gain', 'anxiety',
                              ], multi=False, placeholder="symptoms",
                             clearable=True, optionHeight=50, value='anxiety',
                             style={'color': '#0C34F4', 'fontSize': 14}, id="drp5"),
                html.P([html.U([html.Cite(
                    [html.Button('DiagnoseExplainMatch', id='refer',
                                 style={'backgroundColor': 'F0E68C', 'marginTop': '10px',
                                        'marginRight': '100px', 'marginBottom': '50px',
                                        'marginLeft': '90px',
                                        "border": "2px LightGreen"})], id="cite")])],
                    style={'backgroundColor': 'ff79c6'}),

            ], md=3, sm=12, lg=3, style={'fontSize': 14}),

            dbc.Col([html.P(id='parsed', style={'backgroundColor': 'F0E68C', 'fontSize': 18}),
                     html.Div(dbc.Card(), id="medicine"),
                     html.Div(id="explanations")], md=6, sm=12, lg=6, className="m-5",
                    style={'display': 'inline-block', 'backgroundColor': 'F0E68C',
                           'color': 'LimeGreen', 'fontSize': 14}),

            dbc.Col([html.Div(id="meds"),
                     html.U(),
                     html.Div(id="app1")], md=2, sm=12, lg=2,
                    style={'display': 'inline-block', 'backgroundColor': 'F0E68C',
                           'border': '2px Green', 'marginTop': '20px',
                           'color': 'LimeGreen', 'fontSize': 14})
        ]),
    # html.Br(),
    dbc.Row([
        dbc.Col([
            html.P("Analysis of common Symptoms&Diagnosis"),
            dbc.Card([dbc.CardImg(id="wordcloud")])
        ], className="m-5", md=3, sm=12, lg=3),
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody(id="predictions"),
                ], style={'font-family': 'cursive', 'text-align': 'center', 'color': '#00FFFF',
                          'fontSize': 14})
        ], md=8, sm=12, lg=8)
    ])

], id="container", style={'backgroundColor': 'F0E68C'}, className="m-5", fluid=True)


@app.callback(Output('app1', 'children'),
              Output('parsed', 'children'),
              Output('explanations', 'children'),
              Output('meds', 'children'),
              Output('predictions', 'children'),
              Output('wordcloud', 'src'),
              Input('refer', 'n_clicks'),
              State('drp', 'value'),
              State('drp1', 'value'),
              State('drp2', 'value'),
              State('drp3', 'value'),
              State('drp4', 'value'),
              State('drp5', 'value'), prevent_initial_call=True)
def update_output(n_clicks, state, state0, state1, state2, state3, state4):
    if n_clicks:
        import matching
        from json import loads
        q = state
        w = state0
        e = state1
        r = state2
        t = state3
        y = state4

        # creating out of sample data
        test = {'itching': 0, 'skinrash': 0, 'nodalskineruptions': 0, 'continuoussneezing': 0, 'shivering': 0,
                'chills': 0, 'jointpain': 0, 'stomachpain': 0, 'acidity': 0, 'ulcersontongue': 0,
                'musclewasting': 0, 'vomiting': 0, 'burningmicturition': 0, 'spottingurination': 0,
                'fatigue': 0, 'weightgain': 0, 'anxiety': 0, 'coldhandsandfeets': 0, 'moodswings': 0,
                'weightloss': 0, 'restlessness': 0, 'lethargy': 0, 'smalldentsinnails': 0, 'inflammatorynails': 0,
                'blister': 0, 'redsorearoundnose': 0, 'yellowcrustooze': 0}

        diag = {q.replace(" ", ""): 1, w.replace(" ", ""): 1, e.replace(" ", ""): 1,
                r.replace(" ", ""): 1, t.replace(" ", ""): 1, y.replace(" ", ""): 1}

        recom = {"symptoms": q, "symptoms1": w, "symptoms2": e, "symptoms3": r,
                 "symptoms4": t, "symptoms5": y}

        new_df = {**test, **diag}

        predictor_load = load_smartpredictor('predictor.pkl')

        predictor_load.add_input(x=new_df)

        predictions = predictor_load.data["ypred"].head()

        result = predictions.to_json(orient="split")

        parsed = math.ceil(loads(result)["data"][0][0])

        if parsed == 2:
            parsed = "Allergy",
        elif parsed == 6:
            parsed = "GERD",
        elif parsed == 0:
            parsed = "AIDS",
        elif parsed == 5:
            parsed = "Diabetes",
        elif parsed == 7:
            parsed = "Gastroenteritis",
        elif parsed == 12:
            parsed = "Hypertension",
        elif parsed == 19:
            parsed = "Migraine",
        elif parsed == 17:
            parsed = "Jaundice",
        elif parsed == 18:
            parsed = "Malaria",
        elif parsed == 4:
            parsed = "Dengue",
        elif parsed == 24:
            parsed = "Typhoid",
        elif parsed == 25:
            parsed = "hepatitis A",
        elif parsed == 8:
            parsed = "Hepatitis B",
        elif parsed == 9:
            parsed = "Hepatitis C",
        elif parsed == 10:
            parsed = "Hepatitis D",
        elif parsed == 11:
            parsed = "Hepatitis E",
        elif parsed == 23:
            parsed = "Tuberculosis",
        elif parsed == 21:
            parsed = "Pneumonia",
        elif parsed == 15:
            parsed = "Hypothyroidism",
        elif parsed == 13:
            parsed = "Hyperthyroidism",
        elif parsed == 14:
            parsed = "Hypoglycemia",
        elif parsed == 20:
            parsed = "Osteoarthristis",
        elif parsed == 3:
            parsed = "Arthritis",
        elif parsed == 1:
            parsed = "Acne",
        elif parsed == 22:
            parsed = "Psoriasis",
        elif parsed == 16:
            parsed = "Impetigo",
        else:
            parsed = "Deadly Symptoms, General Hospital Alerted 🚑🏥👩‍🦽"

        dr = matching.condtion_Dr_matching[parsed[0]]

        drBrown = dbc.Card(
            [
                html.Br(),
                dbc.CardImg(src=b64_image(img), top=True),
                dbc.CardBody(
                    [
                        html.H5("Dr.Brown Dad", className="card-title", style={'text-decoration': 'underline'}),
                        html.U(),
                        html.P(
                            html.B(
                                "AIDS, hepatitis A, Hypothyroidism and Impetigo  Specialist"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        html.P(
                            html.B(
                                "Tel: 0789674646"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        dbc.Button("More Details about Dr.Brown", color="primary")
                    ]
                )
            ],
            style={"width": "10rem"}
        ),

        drKen = dbc.Card(
            [
                html.Br(),
                dbc.CardImg(src=b64_image(img1), top=True),
                dbc.CardBody(
                    [
                        html.H5("Dr.Ken Bow", className="card-title", style={'text-decoration': 'underline'}),
                        html.U(),
                        html.P(html.B(
                            "Allergy and Dengue Specialist"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        html.P(html.B(
                            "Tel: 0789674646"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        dbc.Button("More Details about Dr.Ken", color="primary"),
                    ]
                ),
            ],
            style={"width": "10rem"},
        ),

        drEast = dbc.Card(
            [
                html.U(),
                html.Br(),
                dbc.CardImg(src=b64_image(img2), top=True),
                dbc.CardBody(
                    [
                        html.H5("Dr.East Jabali", className="card-title", style={'text-decoration': 'underline'}),
                        html.U(),
                        html.P(html.B(
                            "Acne, TB and Jaundice Specialist"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        html.P(
                            html.B(
                                "Tel: 0789674646"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        dbc.Button("More Details about Dr.East", color="primary"),
                    ]
                )
            ],
            style={"width": "10rem"},
        ),

        drCandice = dbc.Card(
            [
                html.Br(),
                dbc.CardImg(src=b64_image(img3), top=True),
                dbc.CardBody(
                    [
                        html.H5("Dr.Candice Nash", className="card-title", style={'text-decoration': 'underline'}),
                        html.U(),
                        html.P(
                            html.B(
                                "Osteoarthristis, GERD and Typhoid Specialist"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        html.P(
                            html.B("Tel: 0789674646"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        dbc.Button("More Details about Dr.Candice", color="primary")
                    ]
                )
            ],
            style={"width": "10rem"},
        ),

        drWhite = dbc.Card(
            [
                html.Br(),
                dbc.CardImg(src=b64_image(img4), top=True),
                dbc.CardBody(
                    [
                        html.H5("Dr.White Guyo", className="card-title", style={'text-decoration': 'underline'}),
                        html.U(),
                        html.P(
                            html.B(
                                "Diabetes, Hepatitis B and Hyperthyroidism Specialist"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        html.P(
                            html.B("Tel: 0789674646"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        dbc.Button("More Details about Dr.White", color="primary"),
                    ]
                )
            ],
            style={"width": "10rem"},
        ),

        drBlue = dbc.Card(
            [
                html.Br(),
                dbc.CardImg(src=b64_image(img5), top=True),
                dbc.CardBody(
                    [
                        html.H5("Dr.Blue Ang", className="card-title", style={'text-decoration': 'underline'}),
                        html.U(),
                        html.P(
                            html.B(
                                "Hepatitis C, Gastroenteritis and Hypoglycemia Specialist"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        html.P(
                            html.B("Tel: 0789674646"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        dbc.Button("More Details about Dr.Blue", color="primary"),
                    ]
                )
            ],
            style={"width": "10rem"},
        ),

        drEvans = dbc.Card(
            [
                html.Br(),
                dbc.CardImg(src=b64_image(img6), top=True),
                dbc.CardBody(
                    [
                        html.H5("Dr.Eve Nani", className="card-title", style={'text-decoration': 'underline'}),
                        html.U(),
                        html.P(
                            html.B(
                                "Hypertension, Osteoarthristis and Hepatitis D Specialist"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        html.P(
                            html.B("Tel: 0789674646"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        dbc.Button("More Details about Dr.Eve", color="primary"),
                    ]
                ),
            ],
            style={"width": "10rem"},
        ),

        drJane = dbc.Card(
            [
                html.Br(),
                dbc.CardImg(src=b64_image(img7), top=True),
                dbc.CardBody(
                    [
                        html.H5("Dr.jake Louw", className="card-title", style={'text-decoration': 'underline'}),
                        html.U(),
                        html.P(
                            html.B(
                                "Migraine, Hepatitis E and Arthritis Specialist"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        html.P(
                            html.B("Tel: 0789674646"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        dbc.Button("More Details about Dr.Jake", color="primary"),
                    ]
                ),
            ],
            style={"width": "10rem"},
        ),

        drJude = dbc.Card(
            [
                html.Br(),
                dbc.CardImg(src=b64_image(img8), top=True),
                dbc.CardBody(
                    [
                        html.H5("Dr.Jude Ama", className="card-title", style={'text-decoration': 'underline'}),
                        html.U(),
                        html.P(
                            html.B(
                                "Malaria, Psoriasis and Pneumonia Specialist"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),
                        html.P(
                            html.B("Tel: 0789674646"),
                            className="card-text", style={'color': 'Green', 'fontSize': 14}
                        ),

                        dbc.Button("More Details about Dr.Jude", color="primary"),
                    ]
                ),
            ],
            style={"width": "10rem"}
        )

        detailed_contributions = predictor_load.detail_contributions()

        df = detailed_contributions.head()

        df = df[df.columns.difference(["ypred"])]

        df2 = df.transpose()

        color = ["blu", "red", "blue", "gen", "purpl", "orange", "lack", "rd",
                 "bl", "green", "purpe", "ange", "ack", "rd", "ue", "gen",
                 "pple", "onge", "ack", "reed", "bluee", "geen", "purrple", "orrange",
                 "blacck", "rted", "bllue"]

        fig = px.bar(df2, text_auto=True, color=color, width=700, height=700,
                     title="Feature Weights explaining model Decision")

        fig.update_layout(showlegend=False)

        fig.update_layout(
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff')

        fig.update_layout(
            title={
                'text': "Feature Weights explaining model Decision",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

        explaingraph = dcc.Graph(figure=fig, config={'displaylogo': False,
                                                     'modeBarButtonsToRemove': ['lasso2d', 'resetViewMapbox', 'zoom2d',
                                                                                'select2d']})

        diagnose1 = list(parsed)[0]
        diagnose = f"Symptoms suggest: {diagnose1}"

        med = html.Div([html.P(html.B("Medications:")),
                        html.P("☑️Panadol"),
                        html.P("☑️Amoxil"),
                        html.U(), ], id="meds")
        med1 = html.Div([html.P(html.B("Medications:")),
                         html.P("☑️Headex"),
                         html.P("☑️paracetamol"),
                         html.U(), ], id="meds")
        med2 = html.Div([html.P(html.B("Medications:")),
                         html.P("☑️Brufen"),
                         html.P("☑️Amoxil"),
                         html.U(), ], id="meds")
        med3 = html.Div([html.P(html.B("Medications:")),
                         html.P("☑️Penicilin"),
                         html.P("☑️Antibiotics"),
                         html.U(), ], id="meds")
        med4 = html.Div([html.P(html.B("Medications:")),
                         html.P("☑️Paracetamol"),
                         html.P("☑️Action"),
                         html.U(), ], id="meds")
        med5 = html.Div([html.P(html.B("Medications:")),
                         html.P("☑️Flagel"),
                         html.P("☑️Scotts"),
                         html.U(), ], id="meds")
        med6 = html.Div([html.P(html.B("Medications:")),
                         html.P("☑️Scotts"),
                         html.P("☑️Amoxil"),
                         html.U(), ], id="meds")
        med7 = html.Div([html.P(html.B("Medications:")),
                         html.P("☑️Paracetamol"),
                         html.P("☑️Brufen"),
                         html.U(), ], id="meds")
        med8 = html.Div([html.P(html.B("Medications:")),
                         html.P("☑️Eno"),
                         html.P("☑️Action"),
                         html.U(), ], id="meds")

        # Create df for storing live the predictions for audit
        graphDict = {"Recommendation": diagnose1}

        graphPd = pd.DataFrame(graphDict, index=[15])
        graphPd1 = pd.DataFrame(recom, index=[15])

        graph_pd = pd.concat([graphPd1, graphPd], axis=1)

        # Save all the Prompts and the corresponding Recommendations.
        # write the dataframe to a csv file row by row

        graph_pd.to_csv('reco.csv', index=False, mode='a', header=False)

        reco = pd.read_csv("reco.csv")

        wordString = reco.copy()

        wordString = wordString.to_string()

        # Generate a word cloud image
        wordcloud = WordCloud(width=1200, height=800).generate(wordString)

        # Display the generated image
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig("test.jpeg")
        wordCloud = b64_image("test.jpeg")

        dashTable = html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i, "renamable": True, "hideable": True} for i in reco.columns],
                data=reco.to_dict('records'),
                style_table={'overflowX': 'auto'},
                export_format='xlsx',
                editable=True,
                include_headers_on_copy_paste=True,
                sort_action='native',
                page_action="native",
                page_size=8,
                style_cell={
                    'height': 'auto',
                    'minWidth': '140px', 'width': '150px', 'maxWidth': '180px',
                    'whiteSpace': 'normal'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'color': 'black'
                },
                style_data={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'color': 'black'
                }
            )
        ])

        if dr == "drBrown":
            return drBrown, diagnose, explaingraph, med, dashTable, wordCloud
        elif dr == "drWhite":
            return drWhite, diagnose, explaingraph, med1, dashTable, wordCloud
        elif dr == "drCandice":
            return drCandice, diagnose, explaingraph, med2, dashTable, wordCloud
        elif dr == "drJude":
            return drJude, diagnose, explaingraph, med3, dashTable, wordCloud
        elif dr == "drKen":
            return drKen, diagnose, explaingraph, med4, dashTable, wordCloud
        elif dr == "drBlue":
            return drBlue, diagnose, explaingraph, med5, dashTable, wordCloud
        elif dr == "drEvans":
            return drEvans, diagnose, explaingraph, med6, dashTable, wordCloud
        elif dr == "drJane":
            return drJane, diagnose, explaingraph, med7, dashTable, wordCloud
        elif dr == "drEast":
            return drEast, diagnose, explaingraph, med8, dashTable, wordCloud
        else:
            return "No Dr. can treat that condition. OOOpsy! 👩‍🦽🚑🏥"


if __name__ == "__main__":
    app.run_server(debug=True)
