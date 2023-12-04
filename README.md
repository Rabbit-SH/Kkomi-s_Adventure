# Kkomi's_Adventure(Watertoad_Course)
![Service image](images/Service_image/Service_image.jpg)
This code for the watertoad course of the Chiak Mountain Exploration program of the Korea National Park Service.

## Main Function 

### Service Concept

  #### Promoting awareness of the beauty and preservation value of national parks
    
   * Role of National Park Tour Guide: The main purpose is to closely observe the nature and life of the national park and experience the wonders of nature 
   * Highly Autonomous Exploration Service: Highly Autonomous Exploration Service that can be used without tour commentators 
   * Family with children: Targeting families with young children, visiting the center of an experience center, campsite, or the beginning of a national park trail 
   * Minimize media elements: Minimize media elements to help you immerse yourself in walking and observing nature / Media that can be visually interesting is a secondary factor 


## P2GAN
<div style="display: flex; justify-content: center;">
    <img src="images/P2GAN/example1_origin.jpg" alt="P2GAN_example1_origin" width="180" height="180" />
    <img src="images/P2GAN/example1.jpg" alt="P2GAN_example1" width="180" height="180" />
    <img src="images/P2GAN/example2_origin.jpg" alt="P2GAN_example2_origin" width="180" height="180" />
    <img src="images/P2GAN/example2.jpg" alt="P2GAN_example2"width="180" height="180" />
</div>

## AnimeGANv2
<div style="display: flex; justify-content: center;">
    <img src="images/AnimeGANv2/woman2_origin.jpg" alt="Animeganv2_woman2" width="180" height="180" />
    <img src="images/AnimeGANv2/woman2.jpg" alt="Animeganv2_woman2"width="180" height="180" />
    <img src="images/AnimeGANv2/man2_origin.jpg" alt="Animeganv2_man2" width="180" height="180" />
    <img src="images/AnimeGANv2/man2.jpg" alt="Animeganv2_man2"width="180" height="180" />
</div>

## Cartoonizer
<div style="display: flex; justify-content: center;">
    <img src="images/Cartoonizer/example1_origin.jpg" alt="Cartoonizer_example1_origin" width="180" height="180" />
    <img src="images/Cartoonizer/example1.jpg" alt="Cartoonizer_example1" width="180" height="180" />
    <img src="images/Cartoonizer/example2_origin.jpg" alt="Cartoonizer_example2_origin" width="180" height="180" />
    <img src="images/Cartoonizer/example2.jpg" alt="Cartoonizer_example2"width="180" height="180" />
</div>


## Prerequisites

- Windows
- Python 3.7.*
- CPU or NVIDIA GPU + CUDA CuDNN

## Getting Started

- Clone this repo:
```
git clone https://github.com/Rabbit-SH/Kkomi-s_Adventure.git
cd Kkomi-s_Adventure
```
## Install requirements
    
    pip install -r requirements.txt

## Running the Local Server

    uvicorn main:app --reload
    
Then you can test in 127.0.0.1:8000 (localhost)

## How to Use 

### Front-End (For Develper)

    cd b_course/For_Develop
#### Project setup

    npm install
    
#### Compiles and hot-reloads for development

    npm run serve
    
#### Compiles and minifies for production
    npm run build

#### Lints and fixes files

    npm run lint

#### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### Back-End

The frontend receives requests through axios and provides API according to get or post requests.


For example in Vue.js request

    "await axios.post('http://localhost:8000/aipainter', formData,{responseType: 'blob'});" =>

In FastApi

Then the function defined under "@app.post("/aipainter")" is executed and the response is sent back to the frontend.
The frontend receives requests through axios and provides API according to get or post requests.

## For More information 

Check out our other repository here [Kkomi's_Adventure_For_Developer](https://github.com/Rabbit-SH/Untact_Exploration)


## Datasets

P2GAN
```
@misc{pascal-voc-2007,
    author = "Everingham, M. and Van Gool, L. and Williams, CKI and Winn, J. and Zisserman, A.",
    title = "{PASCAL} {V}isual {O}bject {C}lasses {C}hallenge 2007 {(VOC2007)} {R}esults",
    howpublished = "http://www.pascal-network.org/challenges/VOC/voc2007/workshop/index.html"}
```

## Source

Sound source : [에코샵홀씨(주)/김현태](https://wholesee.com/)


## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/Rabbit-SH/Kkomi-s_Adventure/blob/main/LICENSE) file for details

## Related Projects
[AnimeGANv2-pytorch](https://github.com/bryandlee/animegan2-pytorch) | [White-box-Cartoonization](https://github.com/SystemErrorWang/White-box-Cartoonization) | [p2gan](https://github.com/i-evi/p2gan). | [Leaflet](https://github.com/Leaflet/Leaflet) | [Vue](https://github.com/vuejs) | [Vuetify](https://github.com/vuetifyjs/vuetify) | [Vuex](https://github.com/vuejs/vuex) | [Openstreetmap](opendatacommons.org)

## Etc

If you have any questions, please contact us

[Rabbit-SH] : 0324suhyun@gmail.com | <br/>
[Hyewoong] : n417759@gmail.com | <br/>
[cocoball] : wlrn0514@gmail.com | <br/>
[Jinujara] : herjinwo@gmail.com | <br/>
[minjeongKim21] : minddong21@gmail.com 


