

const wrapper__Area = document.querySelector('#wrapper_Area');

const showHidePassDom = Array.from(document.querySelectorAll('.showHide__Icon i'));


// Aside Area
const aside__Area = document.querySelector('#aside_Area');

// Aside Sing-Up & Sign In Buttons
const aside__SignUp_Button = document.querySelector('#aside_signUp_Btn');
const aside__SignIn_Button = document.querySelector('#aside_signIn_Btn');

aside__Area.addEventListener('click', chnageFormMode);
aside__Area.addEventListener('click', chnageFormMode);

// - - - - -  Functions - - - - - //

// Change Form Mode Function
function chnageFormMode(e) {
  // Check. If The Target Element Is Aside Sign-Up Button
  if(e.target === aside__SignUp_Button){
    // Add Class [ Sign Up Mode Active ] On Wrapper Area
    wrapper__Area.classList.add('sign-up__Mode-active');
  };
  // Check. If The Target Element Is Aside Sign-In Button
  if(e.target === aside__SignIn_Button){
    // Remove Class [ Sign Up Mode Active ] From Wrapper Area
    wrapper__Area.classList.remove('sign-up__Mode-active');
  };
};

// Function Show Hide Password
(function showHidePass() {
  // Loop On All The Show Hide Password Icon
  showHidePassDom.forEach(icon =>{
    // When Click On Any Show Hide Icon...
    icon.addEventListener('click', () => {
      // Select The Target Password Input
      const targetAreaInput = icon.parentElement.parentElement.querySelector('.field input');
      // If The Target Icon Has Hide-icon
      if(icon.className === 'bx bx-hide'){
        // Change The Target Icon Class
        icon.className = 'bx bx-show';
        // Change The Target Input Area Type
        targetAreaInput.setAttribute('type', 'text');
      }else{ // else
        // Change The Target Icon Class
        icon.className = 'bx bx-hide';
        // Change The Target Input Area Type
        targetAreaInput.setAttribute('type', 'password');
      };
    });
  });
})();

// Login Form Validation Function
// function loginFormValidation() {
//   // Loop On All The Inputs
//   allLoginFormFields.forEach(input => {
//     // Input Targte Field Name Value
//     const inputAttribueValueName = input.attributes.name.value;
//     // Input Value Without Spaces
//     const inputValue = input.value.trim();
//     // Input Regex Validation Response [ True || False ] :)
//     const inputRegex = patterns[inputAttribueValueName].test(inputValue);

//     // Check If The Input Value Is Empty
//     if(inputValue === ''){
//       // Call Function Set Error For
//       setErrorFor(input, `${inputAttribueValueName} is required. Please enter your response.`);
//     }else if(inputRegex === false){ // Else If: If The InputRegext Response Is False
//       // Call Function Set Error For
//       setErrorFor(input, `${inputAttribueValueName} Is Invalid .`);
//     }else{ // Else
//       // Call Function Set Success For
//       setSuccessFor(input);
//     };
//   });
// };

// Sign-Up Form Validation Function
function signUpFormValidation() {
  // Loop On All The Inputs
  allSignUpFormFields.forEach(input => {
    // Password And Confirm Password Fileds Values Without Spaces
    const passwordFieldValue = passwordField.value.trim();
    const conifrmPassValue = confirmPassword.value.trim();
    // Input Targte Field Name Value
    const inputAttribueValueName = input.attributes.name.value;
    // Input Value Without Spaces
    const inputValue = input.value.trim();
    // Input Regex Validation Response [ True || False ] :)
    const inputRegex = patterns[inputAttribueValueName].test(inputValue);

    // Check If The Input Value Is Empty
    if(inputValue === ''){
      // Call Function Set Error For
      setErrorFor(input, `${inputAttribueValueName} is required. Please enter your response.`);
    }else if(inputRegex === false){ // Else If: If The InputRegext Response Is False
      // Call Function Set Error For
      setErrorFor(input, `${inputAttribueValueName} Is Invalid .`);
    }else{ // Else
      // Call Function Set Success For
      setSuccessFor(input);
    };

    // Validation The Confirm Password
    if(conifrmPassValue === ''){ // Check If The Confirm Password Value Is Empty
      // Call Function Set Error For
      setErrorFor(confirmPassword, `Confirm password is required. Please enter your response.`);
    }else if(conifrmPassValue !== passwordFieldValue){ // Check If The Confirm Password Value Is Dose Not Match The Password Filed
      // Call Function Set Error For
      setErrorFor(confirmPassword, `Confirm password does not match`);
    }else{ // Eles
      // Call Function Set Success For
      setSuccessFor(confirmPassword);
    };

  });
};

// Set Error For Function
function setErrorFor(input, message){
  // Select The Target Parent Target Input Group
  const targetParentInput = input.parentElement.parentElement;
  // Select The Target Input Error Message
  const targetErrorMessage = targetParentInput.querySelector('.input__error_message');

  // Remove Class FormSucess From The Parent Target
  targetParentInput.classList.remove('formSuccess');
  // Add Class Success On Target ParentElement
  targetParentInput.classList.add('formError');
  // Set The Message Inside The Target Error Message
  targetErrorMessage.innerHTML = message;
};

// Set Success For Function
function setSuccessFor(input){
  // Select The Target Parent Target Input Group
  const targetParentInput = input.parentElement.parentElement;
  // Select The Target Input Error Message
  const targetErrorMessage = targetParentInput.querySelector('.input__error_message');

  // Remove Class FormError From The Parent Target
  targetParentInput.classList.remove('formError');
  // Add Class Success On Target ParentElement
  targetParentInput.classList.add('formSuccess');
  // Empty The Error Message
  targetErrorMessage.innerHTML = '';
};