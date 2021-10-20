/*eslint no-undef: "error"*/
/* global gameQuestions, exclude */


<template>
  <!-- <base-container>
    <div v-if="donePickingQuestions">
      <label>Username</label>
      <input placeholder="Enter your username" key="username-input">
    </div>
      <div v-else>
      <label>Email</label>
    <input placeholder="Enter your email address" key="email-input">
    </div>
     <button @click='donePickingQuestions'>Confirm selection!</button>
  </base-container> -->
  
  <base-container v-if="!$store.state.donePickingQuestions">
  <h3>All Questions below</h3> 
  <div>
    <li v-for="(question,index) in isQuestions" :key="index">
          <!-- <input v-model="question.message" :name="questionId(index)"> -->
          {{ question.message }} : state = {{ question.iHave }}
          <button @click="onClick(question.id)"
           >True</button>
    </li>
    <br/>
  </div>
    
  </base-container>

  <base-container v-if="$store.state.donePickingQuestions">
    Displaying Unique UserQuestions : {{ $store.state.displayQuestionsForPlayer1 }}
  </base-container>

  <base-container>
    <button @click="donePickingQuestions() ; getUniqueListBy() ;">Confirm selection!</button>
    <br/>
    <!-- <p>Length of Array : {{ this.$store.state.userQuestions.length }}</p>
    <p>Questions I have clicked True : {{ this.$store.state.userQuestions }}</p> -->
  </base-container>

  <base-container>
      <h3>Pick the correctttt answer </h3>
      <p3> User Score : {{ $store.state.player1Score }}</p3>
      <h1>Picked value is {{ picked }}</h1>
      <div>
        <li v-for="(index, question) in displayQuestionsForPlayer1" :key="question.id">
            {{ question.message }}
            <!-- {{ checkIfCorrectAnswer(picked, question.iHave) }} -->
            {{ pciked }}
            
          <div>  
            <input type="radio" id="true" value="True" v-model="picked">
            <label for="true">True</label>
            <input type="radio" id="false" value="False" v-model="picked">
            <label for="false">False</label>
          </div>
        </li>
      </div>
    </base-container>
    
</template>

<script>
import BaseContainer from './components/BaseContainer.vue';

export default {
  data: function() {
    return {
      pickeds: []
      // isActive: false
    }
  },
  components: {
    BaseContainer
 
  },

methods: {
      // getUniqueListBy(arr, key) {
      //   return [...new Map(arr.map(item => [item[key], item])).values()]
      // },
         checkIfCorrectAnswer(playerPick, answer) {
          if (playerPick == answer) { 
            this.$store.state.player1Score++
            console.log('Player1 pick is : ' + playerPick)
            return this.$store.state.player1Score
            } 
        },
        rewardOnePoint() {
          this.$store.state.player1Score ++;
          console.log('Player 1 Score is : ' + this.$store.state.player1Score)
        },
        getUniqueListBy() {
          const arr = this.$store.state.userQuestions;
          const key = 'id';
          const arr1 = [...new Map(arr.map(item => [item[key], item])).values()];
          arr1.forEach(question => {
            this.$store.state.displayQuestionsForPlayer1.push({
              message: question.message,
              iHave: question.iHave,
              id: question.id
            });
          });
        },
       donePickingQuestions() {
        this.$store.state.donePickingQuestions = !this.$store.state.donePickingQuestions
        this.$store.commit('addQuestionToDisplayQuestions')
        // this.$set(this.$store.donePickingQuestions, false);
        console.log('state of donePickingQuestions : ' + this.$store.state.donePickingQuestions)
        console.log('length of userArray : ' + this.$store.state.userQuestions.length)
      },
      // pickAnswerToQuestion(message. ihave, id) {
      //   this.$store.userQuestions.push({
      //       messagee: message,
      //       ihavee: ihave,
      //       ide: id
      //   })
      // }
    // addOne() {
    //   this.$store.dispatch({
    //     type: 'increase',
    //     value: 10
    //   })
    // },
    // subOne() {
    //     this.$store.commit('decrement')
      onClick(payload) {
        console.log(payload)
        this.$store.commit({
          type: 'changeState',
          value: payload
        });
      },
       gameQuestionsFilter(userQuestionId, allQuestionId) {
        // var allQuestions = this.$store.state.questions;
        // var userQuestions = this.$store.state.userQuestions;
        // allQuestionId.forEach(question => {
        //   console.log('id is : ' + id)
        //     if (id === question.id) {
        //       console.log('true')
        //       return true
        //     } 
        // }
        // ); 
        // console.log('id is : ' + id)
        // console.log('false')
        // return false
        if (userQuestionId == allQuestionId) { return true }
        else { return false }
      }
     },

  computed:  {
      // checkIfCorrectAnswer(playerPick, answer) {
      //     if (playerPick == answer) { 
      //       this.$store.state.player1Score++
      //       return this.$store.state.player1Score
      //       } 
      //   },
      sameId(userId, questionId) {
        if (userId == questionId) {
          return true;
        } else {
          return false;
        }
      },
      isQuestions() {
        return this.$store.state.questions;
      },
      userQuestions() {
        return this.$store.state.userQuestions;
      },
      displayQuestionsForPlayer1() {
        return this.$store.state.displayQuestionsForPlayer1;
      }
      // getUniqueListBy(arr, key) {
      //   return [...new Map(arr.map(item => [item[key], item])).values()]
      // }
  },
  mutations: {
   
  },
  actions: {
 
  }
}
</script>

<style>
/* .btn1 {
  color: white;
  background-color: green;
} */
button.is-active {
  background-color: lightblue;
  border: green solid 2px;
  color: red;
}
</style>