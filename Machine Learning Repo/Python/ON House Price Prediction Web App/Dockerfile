FROM python:3.6-slim
COPY ./templates/00-Basic-Template.html /deploy/templates/
COPY ./templates/map.html /deploy/templates/
COPY ./app.py /deploy/
COPY ./requirements.txt /deploy/
COPY ./engine.pkl /deploy/
COPY ./engine_KNN.pkl /deploy/
COPY ./engine_rf.pkl /deploy/
COPY ./features.pkl /deploy/
COPY ./features_rf.pkl /deploy/
COPY ./mapdict.pkl /deploy/
COPY ./outlier_capper.pkl /deploy/
COPY ./scaler.pkl /deploy/
COPY ./apikey.txt /deploy/
COPY ./KNN.csv /deploy/
WORKDIR /deploy/
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "app.py"]
