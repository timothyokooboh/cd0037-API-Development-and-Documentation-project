import React, { Component } from 'react';
import $ from 'jquery';
import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props) {
    super();
    this.state = {
      question: '',
      answer: '',
      difficulty: 1,
      category: 1,
      categories: {},
      showNotificationForQuestions: false,
      showNotificationForCategories: false,
      newCategory: ""
    };
  }

  componentDidMount() {
    $.ajax({
      url: `/categories`, 
      type: 'GET',
      success: (result) => {
        this.setState({ categories: result.categories });
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again');
        return;
      },
    });
  }

  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/questions', 
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({showNotificationForQuestions: true, question: '', answer: '', difficulty: 1, category: 1});

        setTimeout(() => {
          this.setState({showNotificationForQuestions: false});
        }, 4000)

        document.getElementById('add-question-form').reset();
        return;
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again');
        return;
      },
    });
  };

  submitCategory = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/categories',
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        type: this.state.newCategory,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({ categories: result.categories, showNotificationForCategories: true, newCategory: '' });

        setTimeout(() => {
          this.setState({ showNotificationForCategories: false });
        }, 4000)

        document.getElementById('add-category-form').reset();
        return;
      },
      error: (error) => {
        alert('Unable to add category. Please try your request again');
        return;
      },
    });
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    return (
      <div id='add-form'>
        <h2>Add a New Trivia Question</h2>
        <form
          className='form-view'
          id='add-question-form'
          onSubmit={this.submitQuestion}
        >
          <label>
            Question
            <input type='text' name='question' onChange={this.handleChange} />
          </label>
          <label>
            Answer
            <input type='text' name='answer' onChange={this.handleChange} />
          </label>
          <label>
            Difficulty
            <select name='difficulty' onChange={this.handleChange}>
              <option value='1'>1</option>
              <option value='2'>2</option>
              <option value='3'>3</option>
              <option value='4'>4</option>
              <option value='5'>5</option>
            </select>
          </label>
          <label>
            Category
            <select name='category' onChange={this.handleChange}>
              {Object.keys(this.state.categories).map((id) => {
                return (
                  <option key={id} value={id}>
                    {this.state.categories[id]}
                  </option>
                );
              })}
            </select>
          </label>
          <input type='submit' className='button' value='Submit' disabled={!this.state.question || !this.state.answer} />
        </form>

        { this.state.showNotificationForQuestions && <div className="notification">
          Question added successfully
        </div> }

        <div style={{marginTop: '50px'}}>
          <h2>Add a new category</h2>
          <form onSubmit={this.submitCategory} id='add-category-form'>
            <label>
              Category
              <input type="text" name="newCategory" onChange={this.handleChange} ></input>
            </label>
            <input type="submit" className="button" value="Submit" disabled={!this.state.newCategory} />
          </form>
          { this.state.showNotificationForCategories && <div className="notification">
          Category added successfully
        </div> }

        </div>
      </div>
    );
  }
}

export default FormView;
