import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
    // Domini propi: '/'. El flux de treball d'Actions el sobreescriu amb
    // --base i la sortida base_path de actions/configure-pages.
    base: '/',
    plugins: [tailwindcss()],
    build: {
        outDir: 'dist',
        assetsDir: 'assets',
    },
})
