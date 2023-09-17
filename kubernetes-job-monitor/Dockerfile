FROM python:3.10 as scripting
LABEL author="<Adama DIENG adama.dieng@digitastuces.com>"
WORKDIR /var/www/app
COPY . /var/www/app


FROM nginx:alpine
LABEL author="<Adama DIENG adama.dieng@digitastuces.com>"
COPY --from=scripting /var/www/app/public /usr/share/nginx/html

RUN apk add --no-cache ca-certificates git bash curl jq
RUN apk add py3-pip

ENV KUBECTL_VERSION="v1.15.3"
ENV KUBECTL_SHA256="6e805054a1fb2280abb53f75b57a1b92bf9c66ffe0d2cdcd46e81b079d93c322"
RUN curl -LO "https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" && \
    sha256sum kubectl | grep ${KUBECTL_SHA256} && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/kubectl && \
    mkdir /etc/.kube && \
    touch /etc/.kube/config

WORKDIR /var/www/app

COPY requirements.txt /var/www/app

RUN pip install  --no-cache-dir --upgrade  -r requirements.txt
RUN mkdir -p /run/nginx
COPY --chown=nginx:nginx . /var/www/app

RUN \
  apk update && \
  apk add  supervisor && \
  rm -rf /var/cache/apk/* 

RUN mv .container/start.sh /start.sh && \
    chmod u+x /start.sh && \
    mv .container/nginx.conf /etc/nginx/nginx.conf && \
    chown root:root /etc/nginx/nginx.conf && \
    mv .container/nginx-site.conf /etc/nginx/conf.d/default.conf && \
    chown root:root /etc/nginx/conf.d/default.conf && \
    mv .container/supervisord.conf /etc/supervisord.conf && \
    chown root:root /etc/supervisord.conf && \
    rm -rf .container

EXPOSE 80

ENTRYPOINT ["/bin/bash"]
CMD ["/start.sh"]