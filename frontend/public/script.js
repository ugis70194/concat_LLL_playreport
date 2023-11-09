const fileSelector = document.getElementById("fileselector");
const sumbitButton = document.getElementById("submit");
const alert = document.getElementById("alert");
const image_A = document.getElementById("img_a");
const image_B = document.getElementById("img_b");
const result = document.getElementById("result");

fileSelector.addEventListener("input", readImages, false);
sumbitButton.addEventListener("click", postData, false);

function extCheck(file){
  if(/\.(jpe?g|png)$/i.test(file.name)){
    return false;
  }
  return true;
}

function readFileAsDataURL(file, imgElement){
  const reader = new FileReader();
  reader.onload = function(event){
    imgElement.src = event.target.result;
  }
  reader.readAsDataURL(file);
}

const URL = "https://stitching-sp43hr3pqq-dt.a.run.app"

let postOption = {
  method: "POST",
  headers: {
    'Access-Control-Allow-Origin': "*",
  },
  body: ""
};

async function postData() {
  sumbitButton.disabled = true;

  const formData = new FormData();
  formData.append("img_A", fileSelector.files[0]);
  formData.append("img_B", fileSelector.files[1]);

  postOption.body = formData

  const response = await fetch(URL, postOption);

  //console.log(response);
  res = await response.json();
  //console.log(res);
  result.src = res.result;

  return
}

function init(){
  image_A.src = "";
  image_B.src = "";
  alert.innerText = "";
  sumbitButton.disabled = false;
}

async function readImages(){
  init();

  let files = fileSelector.files;
  if(files.length != 2){
    alert.innerText = "スクリーンショットを2つ選択してください";
    return;
  }

  if(extCheck(files[0]) || extCheck(files[1])){
    alert.innerText = "スクリーンショットは png か jpg 形式にしてください";
    return;
  }

  readFileAsDataURL(files[0], image_A);
  readFileAsDataURL(files[1], image_B);
}