<template>
  <div id="app" class="container grid-lg">
    <div class="columns" style="padding: 2em 0em">
      <div class="column">
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link>
      </div>
    </div>

    <router-view />
  </div>
</template>

