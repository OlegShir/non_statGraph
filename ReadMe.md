<h1 align="center">non-statGraph</h1>

<img src="img/readme/h2.png" width="100%">

## Description  

---

### Theory :mortar_board:

<p align="justify"> The app calculates the probability of being in a certain state of a queuing system with arbitrary distributions of time points between incoming requests and their service time points. The app is based on the use of the Laplace transform and the principle of probabilistic balance when compiling equations for images of the probabilities of the system states. The application allows you to explore the transient process in systems that are called non-stationary. </p>

---

### Features :fire:

---

### Settings :gear:

App settings are set in a file <span style="color:blue">setting.py</span>.

* **DEBUG**: bool - mode of operation, if *True*, outputs intermediate results of calculations to the console (default *True*);  

#### Color :art: 
  
The app uses the RGB color palette.  
  
* **COLOR_SELECTED**: list - color of selected objects (default *yellow [1, 1, 0]*);  
* **COLOR_CONDITION**: list - color of process state (default *white [1, 1, 1]*);   
* **COLOR_TEXT_CONDITION**: color of number of process state (default *black [0, 0, 0]*);  
* **COLOR_COUNTER_CONDITION**: list - color of outer contour of process state (default *blue [0, 0, 1]*);  
* **COLOR_CONNECTOR**: list - color of process state connectors (default *red [1, 1, 1]*);  
* **COLOR_BGR**: list - app background color, color palette **RGBA** (default *black [0, 0, 0, 0]*);  
* **COLOR_BEZIE_LINE**: list - color of lines connecting process states (default *white [1, 1, 1]*);   
* **COLOR_TEXT**: list - color of text other elements (default *white [1, 1, 1]*);  
  
#### Size :triangular_ruler:
  
The app uses pixels as the unit of measurement.   
  
* **WIDTH_LIGHTER**: int - width of highlighter line of process state (default *3*);  
* **WIDTH_COUNTER**: int - width of outer contour of process state (default *1*);  
* **SIZE_ARROW**: int - size of arrow of lines connecting process states (default *10*);  
* **SIZE_BTN**: tuple - size of all button app, length*height, (default *(150, 60)*);
* **RADIUS_CONDITION**: int - radius of process state (default *50*);  
* **RADIUS_CONNECTOR**: int - radius of process state connectors  (default *5*);  
* **RADIUS_BEZIER_POINT**: int - radius of point of lines connecting process states (default *5*);   

#### Fonts :pencil:

* **FONT_SIZE_LABEL_CONDITION**: int - fontsize of number process state (default *60*);  
* **FONT_SIZE_LAW_PARAM**: int - fontsize of text distribution law (default *18*);  
* **FONT_SIZE_MESSAGE_TO_USER**: int - fontsize of text message to user (default *14*);  

--- 

### Requirements

Installing packages: **pip install -r requirements.txt**  

General:  
* Kivy  
* Sympy  
* Scipy
* Matplotlib  

---

TAGS :lab1el:: laplace, state of system, distribution laws, graphs, Dirac, delta function
