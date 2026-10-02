import streamlit as st
import os
import pandas as pd
from datetime import datetime
from src import get_all_history, save_submission, delete_submission , caption_image , classify_text


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "assets", "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)



CLASSES = [
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate"
]




with st.sidebar:
    st.title("Navigation")

    app_mode = st.radio(
        "Go to:",
        ["Evaluation Workspace", "History Logs"]
    )


if app_mode == "Evaluation Workspace":

    st.title("Content Classification Portal")
    st.write("Submit text comments or upload image.")

    st.markdown(
        """
        <style>
            .stFileUploader label {
                display: none;
            }

            .stFileUploader section {
                padding: 0 !important;
                min-height: unset !important;
                border: none !important;
                background: transparent !important;
            }

            .stFileUploader section div div {
                display: none;
            }

            div[data-testid="stHorizontalBlock"] {
                align-items: center !important;
                gap: 10px !important;
            }

            .prediction-container {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 8px;
            }

            .prediction-badge {
                padding: 5px 10px;
                border-radius: 7px;
                background: rgba(220, 53, 69, 0.12);
                border: 1px solid rgba(220, 53, 69, 0.25);
                font-size: 13px;
                font-weight: 600;
            }

            .no-prediction {
                opacity: 0.6;
            }

            .history-id {
                font-weight: 600;
                opacity: 0.8;
            }

            .history-type {
                font-weight: 500;
                text-transform: capitalize;
            }

            .history-text {
                max-width: 280px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            .history-path {
                max-width: 300px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                opacity: 0.75;
            }

            .history-badges {
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
            }

            .history-badge {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 6px;
                background: rgba(220, 53, 69, 0.12);
                border: 1px solid rgba(220, 53, 69, 0.20);
                font-size: 12px;
                font-weight: 600;
            }

            .history-empty {
                opacity: 0.5;
            }

            .history-time {
                white-space: wrap;
                opacity: 0.75;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    input_col, file_col = st.columns([0.90, 0.10])

    with file_col:
        uploaded_file = st.file_uploader(
            "Upload",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )

    with input_col:
        
        chat_text = st.chat_input("Type your message here...")

    content_type = None
    user_payload = None
    saved_img_path = None
    processed_text = None

    if chat_text:
        content_type = "text"
        user_payload = chat_text
        processed_text = chat_text

    elif uploaded_file:
        content_type = "image"

        filename = (
            f"{int(datetime.now().timestamp() * 1000)}_"
            f"{uploaded_file.name}"
        )

        absolute_img_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        with open(absolute_img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        saved_img_path = os.path.join(
            "assets",
            "uploads",
            filename
        )

        user_payload = saved_img_path

        processed_text = caption_image(
            absolute_img_path
        )

    if content_type:

        prediction = classify_text(
            processed_text
        )

        save_submission(
            content_type,
            chat_text,
            saved_img_path,
            prediction
        )

        st.markdown("---")
        st.subheader("Analysis Result")

        if content_type == "image":

            st.image(
                uploaded_file,
                caption="Analyzed Image Source",
                width=350
            )

            st.info(
                f"**Extracted Caption:** {processed_text}"
            )

        else:

            st.markdown(
                f'**Submitted User Text:** *"{user_payload}"*'
            )

        st.markdown("### Detected Classes")

        if prediction:

            badges = "".join(
                f'<span class="prediction-badge">'
                f'{label}'
                f'</span>'
                for label in prediction
            )

            st.markdown(
                f'<div class="prediction-container">'
                f'{badges}'
                f'</div>',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                '<span class="no-prediction">'
                'No detected classes'
                '</span>',
                unsafe_allow_html=True
            )


else:

    st.title("System Audit History")

    history_df = get_all_history()

    if not history_df.empty:

        col1, col2 = st.columns(2)

        col1.metric(
            "Total Submissions",
            len(history_df)
        )

        total_detected = 0

        for value in history_df["prediction"]:

            if pd.isna(value):
                continue

            try:
                parsed_prediction = eval(str(value))

                if isinstance(parsed_prediction, list):
                    total_detected += len(parsed_prediction)

            except:
                pass

        col2.metric(
            "Detected Classes",
            total_detected
        )

        st.markdown("---")
        st.subheader("Submission History")

        st.markdown(
            """
            <style>
                .history-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                    font-size: 14px;
                }

                .history-table th {
                    text-align: left;
                    padding: 12px 10px;
                    border-bottom: 2px solid rgba(128,128,128,0.35);
                    font-weight: 600;
                }

                .history-table td {
                    padding: 11px 10px;
                    border-bottom: 1px solid rgba(128,128,128,0.18);
                    vertical-align: middle;
                }

                .history-table tr:hover {
                    background-color: rgba(128,128,128,0.06);
                }

                .history-id {
                    font-weight: 600;
                    opacity: 0.8;
                }

                .history-type {
                    font-weight: 500;
                    text-transform: capitalize;
                }

                .history-text {
                    max-width: 280px;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                }

                .history-path {
                    max-width: 300px;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                    opacity: 0.75;
                }

                .history-badges {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 5px;
                }

                .history-badge {
                    display: inline-block;
                    padding: 4px 8px;
                    border-radius: 6px;
                    background: rgba(220, 53, 69, 0.12);
                    border: 1px solid rgba(220, 53, 69, 0.20);
                    font-size: 12px;
                    font-weight: 600;
                }

                .history-empty {
                    opacity: 0.5;
                }

                .history-time {
                    white-space: wrap;
                    opacity: 0.75;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        header_columns = st.columns(
            [0.45, 0.8, 1.5, 2.5, 1.3, 1.3, 1.2]
        )

        headers = [
            "ID",
            "Type",
            "Input",
            "File Path",
            "Prediction",
            "Timestamp",
            "Action"
        ]

        for column, header in zip(
            header_columns,
            headers
        ):

            with column:
                st.markdown(
                    f"**{header}**"
                )

        st.divider()

        for row_position, (_, row) in enumerate(
            history_df.iterrows()
        ):

            row_columns = st.columns(
                [0.45, 0.8, 2.5, 2.5, 1.0, 1.6, 0.8]
            )

            record_id = int(row["id"])

            content_type = str(
                row["content_type"]
            )

            input_text = row["input_text"]

            if pd.isna(input_text):
                input_text = ""

            input_text = str(input_text)

            file_path = row["file_path"]

            if pd.isna(file_path):
                file_path = ""

            file_path = str(file_path)

            timestamp = str(
                row["timestamp"]
            )

            prediction_value = row["prediction"]

            try:

                if pd.isna(prediction_value):

                    predictions = []

                else:

                    predictions = eval(
                        str(prediction_value)
                    )

                    if not isinstance(
                        predictions,
                        list
                    ):
                        predictions = []

            except:

                predictions = []

            with row_columns[0]:

                st.markdown(
                    f'<span class="history-id">'
                    f'{record_id}'
                    f'</span>',
                    unsafe_allow_html=True
                )

            with row_columns[1]:

                st.markdown(
                    f'<span class="history-type">'
                    f'{content_type}'
                    f'</span>',
                    unsafe_allow_html=True
                )

            with row_columns[2]:

                if input_text:

                    display_text = (
                        input_text
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                    )

                    st.markdown(
                        f'<div class="history-text" '
                        f'title="{display_text}">'
                        f'{display_text}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                else:

                    st.caption("—")

            with row_columns[3]:

                if file_path:

                    display_path = (
                        file_path
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                    )

                    st.markdown(
                        f'<div class="history-path" '
                        f'title="{display_path}">'
                        f'{display_path}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                else:

                    st.caption("—")

            with row_columns[4]:

                if predictions:

                    badges = "".join(
                        f'<span class="history-badge">'
                        f'{label}'
                        f'</span>'
                        for label in predictions
                    )

                    st.markdown(
                        f'<div class="history-badges">'
                        f'{badges}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        '<span class="history-empty">'
                        'No detected classes'
                        '</span>',
                        unsafe_allow_html=True
                    )

            with row_columns[5]:

                st.markdown(
                    f'<span class="history-time">'
                    f'{timestamp}'
                    f'</span>',
                    unsafe_allow_html=True
                )

            with row_columns[6]:

                if st.button(
                    "Delete",
                    key=f"delete_{record_id}_{row_position}",
                    type="secondary"
                ):

                    if delete_submission(record_id):

                        st.rerun()

    else:

        st.info(
            "The history logs are empty."
        )