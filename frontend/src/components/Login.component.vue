<template>
  <v-layout
    align-center
    justify-center>
    <v-flex
      xs12
      sm8
      md5>
      <v-card
        color="black"
      >
        <!-- <v-toolbar
          dark>
          <v-toolbar-title>Login</v-toolbar-title>
        </v-toolbar> -->
        <v-card-title primary-title>
          <div
            class="headline"
            style="color: goldenrod"
          >Login</div>
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              v-model="username"
              prepend-icon="person"
              name="username"
              label="Username"
              type="text"
              data-vv-name="username"/>
            <v-text-field
              id="password"
              v-model="password"
              prepend-icon="lock"
              name="password"
              label="Password"
              type="password"
              data-vv-name="password"/>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn
            color="primary"
            flat
            @click="login"
          >Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import AuthController from 'Controllers/auth.controller';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    login() {
      AuthController.login({
        username: this.username,
        password: this.password
      }).catch(() => {
        this.$alert.error('Error! Check your credentials.');
      });
    }
  }
};
</script>
