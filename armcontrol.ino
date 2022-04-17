#include <Servo.h>

Servo base;
Servo leg;
Servo body;
Servo arml;
Servo armr;
Servo claw;

int pos =0;

void setup() {
  //declaring digital I/O pins as Input or Output 
  pinMode(3, OUTPUT);    
  pinMode(5, OUTPUT);    
  pinMode(6, OUTPUT);    
  pinMode(9, OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(7, OUTPUT);                 // sends signal to de10 Nano
  pinMode(4, INPUT);                  // recieves signal from de10 Nano
  
//assigning control/position pin of the servo motors to the PWM signal pins of the arduino 
  base.attach(3);
  leg.attach(5);
  body.attach(6);
  arml.attach(9);
  armr.attach(10);
  claw.attach(11);
//fixing the initial position of all servo motors of the robotic arm
  base.write(90);
  body.write(90);
  leg.write(180);
  arml.write(90);
  armr.write(90);
  claw.write(70);
}

void loop(){
  if(digitalRead(4)==HIGH){
  // robotic arm gets into plucking position from initial
  for(pos=180;pos>=90;pos-=2){
    leg.write(pos);
    delay(15);}
  delay(1500);
  for(pos=90;pos>=0;pos-=2){
    base.write(pos);
    delay(15);}
  delay(1500);
 
  //starts plucking
  for(pos=180;pos>=90;pos-=1){        //plucking claw plucks the plant        
    arml.write(180-pos);
    armr.write(pos);
    delay(10);}
  delay(1500);
  for(pos=90;pos>=10;pos-=2){         //body moves down for picking position
    body.write(pos);
    delay(15);}
  delay(1500);
  for(pos=90;pos>=30;pos-=1){         //leg moves down for picking position
    leg.write(pos);
    delay(15);}
  delay(1000);
  for(pos=70;pos>=0;pos-=2){          //claw holds the plant
    claw.write(pos);
    delay(10);}
  delay(1500);
  for(pos=30;pos<50;pos+=2){          //leg moves up after picking up the plant
    leg.write(pos);
    delay(15);}
  delay(1500);
  for(pos=50;pos<=90;pos+=2){         //leg and body moves up together after picking the plant
    body.write(2*pos);
    leg.write(pos);
    delay(15);}
  delay(1500);
  for(pos=0;pos<=140;pos+=1){         //base of the arm rotates to storage position 
    base.write(pos);
    delay(15);}
  delay(1000);
  for(pos=0;pos<=70;pos+=2){          //claw releases the plant in the container
    claw.write(pos);
    delay(10);}
  delay(1500);
  for(pos=140;pos>=0;pos-=1){         //base of the arm returns back to original position
    base.write(pos);
    delay(15);}  
  delay(1500);
  digitalWrite(7, HIGH);              //sending signal to de10 Nano that plant is plucked and stored successfully  
  delay(1500);
  digitalWrite(7, LOW);  
//robotic arm goes back to initial position 
  for(pos=90;pos<=180;pos+=2){
    leg.write(pos);
    delay(15);}
  delay(1500);
  for(pos=0;pos<=90;pos+=2){
    base.write(pos);
    delay(15);}
  delay(1500);}             
  else{                              
//holding claw opens and closes while searching for medicinal plant 
    for(pos=70;pos>=0;pos-=2){         
    claw.write(pos);
    delay(10);}
  delay(1500);
  for(pos=0;pos<=70;pos+=2){        
    claw.write(pos);
    delay(10);}
  delay(1500);} 
}
 
  
  
  
