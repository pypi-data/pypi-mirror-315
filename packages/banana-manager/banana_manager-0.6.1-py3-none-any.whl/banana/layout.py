from dash import dcc, html
from dash_ag_grid import AgGrid
from dash_iconify import DashIconify
import dash_mantine_components as dmc

from .core.config import config


class Layout(dmc.MantineProvider):
    def __init__(self):
        super().__init__(
            html.Div(
                [
                    dcc.Location(id="banana--location", refresh=True),
                    dcc.Store(id="banana--refresh-table", data=0),
                    dmc.NotificationProvider(position="bottom-center"),
                    html.Div(id="banana--notification"),
                    self.history_modal(),
                    self.insert_modal(),
                    self.left_section(),
                    self.right_section(),
                ],
                className="container",
            )
        )

    def left_section(self) -> html.Div:
        return dmc.Paper(
            children=[
                html.Div(id="banana--menu"),
                dmc.Button(
                    "Refresh",
                    id="banana--refresh-button",
                    color=config.theme,
                    radius="md",
                    leftSection=DashIconify(icon="mingcute:refresh-3-fill", height=20),
                    variant="light",
                    mt=20,
                ),
            ],
            className="left-section",
            bg=dmc.DEFAULT_THEME["colors"][config.theme][9],
        )

    def right_section(self) -> html.Div:
        return html.Div(
            html.Div(
                [
                    self.right_section_header(),
                    AgGrid(
                        id="banana--table",
                        style={"height": "calc(100vh - 85px)", "overflow": "auto"},
                    ),
                ],
                className="content",
            ),
            className="right-section",
        )

    def right_section_header(self) -> dmc.Group:
        return dmc.Group(
            [
                dmc.Text(
                    "No table selected",
                    id="banana--table-title",
                    className="table-title",
                    c=dmc.DEFAULT_THEME["colors"][config.theme][9],
                ),
                dmc.Group(
                    [
                        dmc.Button(
                            "Insert",
                            id="banana--insert-button",
                            color="green",
                            radius="md",
                            leftSection=DashIconify(
                                icon="mingcute:add-circle-fill", height=20
                            ),
                        ),
                        dmc.Button(
                            "History",
                            id="banana--history-button",
                            color="dark",
                            radius="md",
                            leftSection=DashIconify(
                                icon="mingcute:history-anticlockwise-fill", height=20
                            ),
                        ),
                    ]
                ),
            ],
            justify="space-between",
        )

    def insert_modal(self) -> dmc.Modal:
        return dmc.Modal(
            [
                dmc.SimpleGrid(id="banana--insert-form", cols=2),
                dmc.Center(
                    [
                        dmc.Button(
                            "Cancel",
                            id="banana--insert-cancel",
                            color="red",
                            radius="md",
                            variant="subtle",
                            leftSection=DashIconify(
                                icon="mingcute:close-circle-fill",
                                height=20,
                            ),
                            mr=10,
                        ),
                        dmc.Button(
                            "Confirm",
                            id="banana--insert-confirm",
                            color="green",
                            radius="md",
                            leftSection=DashIconify(
                                icon="mingcute:add-circle-fill",
                                height=20,
                            ),
                        ),
                    ],
                    mt=20,
                ),
            ],
            id="banana--insert-modal",
            opened=False,
        )

    def history_modal(self) -> dmc.Modal:
        return dmc.Modal(
            title="Change log",
            id="banana--history-modal",
            size="xl",
            radius="md",
        )
