import { createApp } from 'vue';
import { createStore } from 'vuex';

import App from './App.vue';

const store = createStore({
  state() {
    return {
      questions: [
        { message: 'Never have i ever been to france', iHave: false, id: 1 },
        { message: 'Never have i ever been to colombia', iHave: false, id: 2 },
        { message: 'Never have i ever been to thailand', iHave: false, id: 3 },
        { message: 'Never have i ever been to China', iHave: false, id: 4 }
      ],
      // question: false,
      userQuestions: [],
      finalQuestions: [],
      displayQuestionsForPlayer1: [],
      donePickingQuestions: false,
      player1Score: 0
    };
  },
  mutations: {
    // getUniqueListBy(arr, key) {
    //   const arr1 = [...new Map(arr.map(item => [item[key], item])).values()];
    //   arr1.forEach(question => {
    //     this.$store.state.displayQuestionsForPlayer1.push({
    //       message: question.message,
    //       iHave: question.iHave,
    //       id: question.id
    //     });
    //   });
    // },
    changeState(state, payload) {
      var m = state.questions;
      m.forEach(question => {
        console.log('id is : ' + question.id);
        console.log('message is : ' + question.message);
        console.log('payload (id) :' + payload.value);
        if (question.id == payload.value) {
          question.iHave = true;
          state.userQuestions.push({
            message: question.message,
            iHave: question.iHave,
            id: question.id
          });
        }
      });
    },
    addQuestionToDisplayQuestions(state) {
      // payload is length of array
      var m = state.userQuestions;
      var n = state.questions;

      n.forEach(allQuestion => {
        m.forEach(userQuestion => {
          if (allQuestion.id == userQuestion.id) {
            return;
          } else if (n.includes(userQuestion)) {
            console.log('contains and works!!');
            return;
          } else {
            state.userQuestions.push({
              message: allQuestion.message,
              iHave: allQuestion.iHave,
              id: allQuestion.id
            });
          }
        });
      });
    }
  },
  actions: {
    addQuestionToDisplayQuestions(context) {
      context.commit('addQuestionToDisplayQuestions');
    }
  },
  getters: {
    userDisplayQuestions(state) {
      return state.displayQuestions;
    }
  }
});

const app = createApp(App);

app.use(store);

app.mount('#app');
