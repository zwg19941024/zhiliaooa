<template>
    <div> <!-- 页面内容 --> </div>
</template>
<script>
import { Config, PixelStreaming } from '@epicgames-ps/lib-pixelstreamingfrontend-ue5.3';
import { Application, PixelStreamingApplicationStyle } from '@epicgames-ps/lib-pixelstreamingfrontend-ui-ue5.3';
export default {
    name: 'PlayerView', mounted() {
        const PixelStreamingApplicationStyles = new PixelStreamingApplicationStyle();
        PixelStreamingApplicationStyles.applyStyleSheet();
        const config = new Config({ useUrlParams: true });
        const stream = new PixelStreaming(config);
        const application = new Application({ stream, onColorModeChanged: (isLightMode) => PixelStreamingApplicationStyles.setColorMode(isLightMode) });
        document.body.appendChild(application.rootElement);
    },
    methods: {
        // ...    
    }
}</script>
<style>
body {
    width: 100vw;
    height: 100vh;
    min-height: -webkit-fill-available;
    font-family: 'Montserrat';
    margin: 0;
}
</style>
