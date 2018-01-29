from fabric.api import local

def webpack():
    local('rm -rf static/RSR/bundles/stage/*')
    local('rm -rf static/RSR/bundles/prod/*')
    local('node_modules/.bin/webpack --config webpack.stage.config.js --progress --colors')
    local('node_modules/.bin/webpack --config webpack.prod.config.js --progress --colors')
