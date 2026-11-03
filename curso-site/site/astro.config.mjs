// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
export default defineConfig({
  site: 'https://bfrpaulondev.github.io', base: '/curso-sentinel', trailingSlash: 'always',
  integrations: [starlight({
    title: 'Sentinel na prática', defaultLocale: 'root', locales: { root: { label: 'Português do Brasil', lang: 'pt-BR' } },
    social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/bfrpaulondev/curso-sentinel' }],
    customCss: ['./src/styles/curso.css'],
    head: [{ tag: 'script', content: "window.CS_BASE='/curso-sentinel/'" }, { tag: 'script', attrs: { src: '/curso-sentinel/js/chart.umd.js', defer: true } }, { tag: 'script', attrs: { src: '/curso-sentinel/js/curso.js', defer: true } }],
    sidebar: [
      { label: 'Módulo 0 — Laboratório', autogenerate: { directory: 'm0' } },
      { label: 'Módulo 2 — KQL', autogenerate: { directory: 'm2' } },
      { label: 'Módulo 4 — Detecção', autogenerate: { directory: 'm4' } },
      { label: 'Extras', items: [{ label: 'Glossário', link: '/glossario/' }, { label: 'Playground KQL', link: '/playground/' }, { label: 'O que é real', link: '/sobre/' }] },
    ],
  })],
});
