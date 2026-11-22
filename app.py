import sys
import random
import time
from collections import deque
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QComboBox, 
                             QSlider, QPushButton, QLabel, QToolBar)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QSurfaceFormat, QMouseEvent, QWheelEvent
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *

# ================================================================
# ELEMENT CONSTANTS
# ================================================================
EMPTY, SAND, WATER, FIRE, SMOKE, LAVA, OIL, ACID = 0, 1, 2, 3, 4, 5, 6, 7
STONE, WOOD, GUNPOWDER, STEAM, ICE, PLANT, GAS, VOID_E = 8, 9, 10, 11, 12, 13, 14, 15
SALT, DUST, MUD, GLASS, CLONE, EMBER, THERMITE = 16, 17, 18, 19, 20, 21, 22
SNOW, ASH, COAL, GRAVEL, SEED, SULFUR = 23, 24, 25, 26, 27, 28
MERCURY, NAPALM, SLIME, POISON, NITRO = 29, 30, 31, 32, 33
HYDROGEN, TOXIC_GAS, NITROUS, CONFETTI = 34, 35, 36, 37
METAL, RUST, CONCRETE, RUBBER, COTTON, WAX, FUSE, COBWEB, COPPER, DYNAMITE = 38, 39, 40, 41, 42, 43, 44, 45, 46, 47
MOLTEN_METAL, SPARK, METHANE = 48, 49, 50
BLOOD, LICHEN, FUNGUS, MAGNESIUM, CHARCOAL = 51, 52, 53, 54, 55
RESIN, BRICK, MOSAIC, BUBBLE, OZONE = 56, 57, 58, 59, 60
PLASMA, COTTON_CANDY, DARK_MATTER, HONEY, BONE = 61, 62, 63, 64, 65
TAR, VINE, DRY_ICE, CO2, PHOSPHORUS = 66, 67, 68, 69, 70
GRAIN, FAT, AMBER, INK, RADIOACTIVE = 71, 72, 73, 74, 75
FEATHER, GLACIER, ELECTRICAL, MUDSTONE, ANTIMATTER = 76, 77, 78, 79, 80

ELEMS = [
    {"id": EMPTY, "name": "Eraser", "key": "0", "group": "Tools"},
    {"id": SAND, "name": "Sand", "key": "1", "group": "Powders"},
    {"id": SALT, "name": "Salt", "key": "", "group": "Powders"},
    {"id": GUNPOWDER, "name": "Gunpowder", "key": "G", "group": "Powders"},
    {"id": DUST, "name": "Dust", "key": "", "group": "Powders"},
    {"id": THERMITE, "name": "Thermite", "key": "T", "group": "Powders"},
    {"id": SNOW, "name": "Snow", "key": "", "group": "Powders"},
    {"id": ASH, "name": "Ash", "key": "", "group": "Powders"},
    {"id": COAL, "name": "Coal", "key": "", "group": "Powders"},
    {"id": GRAVEL, "name": "Gravel", "key": "", "group": "Powders"},
    {"id": SEED, "name": "Seed", "key": "", "group": "Powders"},
    {"id": SULFUR, "name": "Sulfur", "key": "", "group": "Powders"},
    {"id": WATER, "name": "Water", "key": "2", "group": "Liquids"},
    {"id": OIL, "name": "Oil", "key": "6", "group": "Liquids"},
    {"id": ACID, "name": "Acid", "key": "7", "group": "Liquids"},
    {"id": LAVA, "name": "Lava", "key": "5", "group": "Liquids"},
    {"id": MUD, "name": "Mud", "key": "M", "group": "Liquids"},
    {"id": MERCURY, "name": "Mercury", "key": "", "group": "Liquids"},
    {"id": NAPALM, "name": "Napalm", "key": "N", "group": "Liquids"},
    {"id": SLIME, "name": "Slime", "key": "", "group": "Liquids"},
    {"id": POISON, "name": "Poison", "key": "", "group": "Liquids"},
    {"id": NITRO, "name": "Nitro", "key": "", "group": "Liquids"},
    {"id": MOLTEN_METAL, "name": "Molten Metal", "key": "", "group": "Liquids"},
    {"id": FIRE, "name": "Fire", "key": "3", "group": "Gases"},
    {"id": SMOKE, "name": "Smoke", "key": "4", "group": "Gases"},
    {"id": STEAM, "name": "Steam", "key": "", "group": "Gases"},
    {"id": GAS, "name": "Gas", "key": "", "group": "Gases"},
    {"id": EMBER, "name": "Ember", "key": "E", "group": "Gases"},
    {"id": HYDROGEN, "name": "Hydrogen", "key": "H", "group": "Gases"},
    {"id": TOXIC_GAS, "name": "Toxic Gas", "key": "", "group": "Gases"},
    {"id": NITROUS, "name": "Nitrous", "key": "", "group": "Gases"},
    {"id": CONFETTI, "name": "Confetti", "key": "", "group": "Gases"},
    {"id": STONE, "name": "Stone", "key": "8", "group": "Solids"},
    {"id": WOOD, "name": "Wood", "key": "9", "group": "Solids"},
    {"id": ICE, "name": "Ice", "key": "I", "group": "Solids"},
    {"id": GLASS, "name": "Glass", "key": "", "group": "Solids"},
    {"id": PLANT, "name": "Plant", "key": "P", "group": "Solids"},
    {"id": METAL, "name": "Metal", "key": "", "group": "Solids"},
    {"id": RUST, "name": "Rust", "key": "", "group": "Solids"},
    {"id": CONCRETE, "name": "Concrete", "key": "", "group": "Solids"},
    {"id": RUBBER, "name": "Rubber", "key": "", "group": "Solids"},
    {"id": COTTON, "name": "Cotton", "key": "", "group": "Solids"},
    {"id": WAX, "name": "Wax", "key": "", "group": "Solids"},
    {"id": FUSE, "name": "Fuse", "key": "F", "group": "Solids"},
    {"id": COBWEB, "name": "Cobweb", "key": "", "group": "Solids"},
    {"id": COPPER, "name": "Copper", "key": "", "group": "Solids"},
    {"id": DYNAMITE, "name": "Dynamite", "key": "D", "group": "Solids"},
    {"id": CLONE, "name": "Clone", "key": "", "group": "Special"},
    {"id": VOID_E, "name": "Void", "key": "V", "group": "Special"},
    {"id": SPARK, "name": "Spark", "key": "S", "group": "Special"},
    {"id": METHANE, "name": "Methane", "key": "", "group": "Special"},
    {"id": BLOOD, "name": "Blood", "key": "B", "group": "Liquids"},
    {"id": HONEY, "name": "Honey", "key": "", "group": "Liquids"},
    {"id": LICHEN, "name": "Lichen", "key": "L", "group": "Solids"},
    {"id": FUNGUS, "name": "Fungus", "key": "", "group": "Solids"},
    {"id": MAGNESIUM, "name": "Magnesium", "key": "", "group": "Solids"},
    {"id": CHARCOAL, "name": "Charcoal", "key": "", "group": "Solids"},
    {"id": RESIN, "name": "Resin", "key": "", "group": "Solids"},
    {"id": BRICK, "name": "Brick", "key": "", "group": "Solids"},
    {"id": MOSAIC, "name": "Mosaic", "key": "", "group": "Solids"},
    {"id": BONE, "name": "Bone", "key": "", "group": "Solids"},
    {"id": BUBBLE, "name": "Bubble", "key": "", "group": "Gases"},
    {"id": OZONE, "name": "Ozone", "key": "O", "group": "Gases"},
    {"id": PLASMA, "name": "Plasma", "key": "", "group": "Gases"},
    {"id": COTTON_CANDY, "name": "Candy", "key": "", "group": "Gases"},
    {"id": DARK_MATTER, "name": "Dark Matter", "key": "", "group": "Special"},
    {"id": TAR, "name": "Tar", "key": "", "group": "Liquids"},
    {"id": INK, "name": "Ink", "key": "", "group": "Liquids"},
    {"id": VINE, "name": "Vine", "key": "", "group": "Solids"},
    {"id": DRY_ICE, "name": "Dry Ice", "key": "", "group": "Solids"},
    {"id": PHOSPHORUS, "name": "Phosphorus", "key": "", "group": "Powders"},
    {"id": GRAIN, "name": "Grain", "key": "", "group": "Powders"},
    {"id": FAT, "name": "Fat", "key": "", "group": "Solids"},
    {"id": AMBER, "name": "Amber", "key": "", "group": "Solids"},
    {"id": RADIOACTIVE, "name": "Radioactive", "key": "R", "group": "Solids"},
    {"id": GLACIER, "name": "Glacier", "key": "", "group": "Solids"},
    {"id": MUDSTONE, "name": "Mudstone", "key": "", "group": "Solids"},
    {"id": CO2, "name": "CO2", "key": "", "group": "Gases"},
    {"id": FEATHER, "name": "Feather", "key": "", "group": "Gases"},
    {"id": ELECTRICAL, "name": "Electrical", "key": "", "group": "Gases"},
    {"id": ANTIMATTER, "name": "Antimatter", "key": "", "group": "Special"},
]

# Element ID -> name lookup (for hover info, eyedropper, status bar)
ELEM_NAME = {e["id"]: e["name"] for e in ELEMS}
ELEM_NAME[EMPTY] = "Empty"

# Element ID -> key lookup (for shortcut display)
ELEM_KEY = {e["id"]: e["key"] for e in ELEMS if e["key"]}

# ================================================================
# GLSL SHADERS  (redesigned — single packed RGBA8 data texture)
# ================================================================
VERT_SRC = """
#version 460 core
layout(location=0) in vec2 aPos;
out vec2 vUv;
void main() {
    vUv = aPos * 0.5 + 0.5;
    gl_Position = vec4(aPos, 0.0, 1.0);
}
"""

# --- scene colouring ---------------------------------------------------
# Reads ONE sampler2D: R=type(0-80)  G=var(0-255)  B=life_lo  A=life_hi
FRAG_SRC = """
#version 460 core
in vec2 vUv;
out vec4 FragColor;
uniform sampler2D u_data;
uniform float u_time;
uniform vec2  u_res;

float hash21(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}

vec3 elemColor(uint t, float v, float life, vec2 px){
    float x=px.x, y=px.y, f=u_time;
    vec3 c;
    switch(t){
    /* ---- powders ---- */
    case  1u: c=vec3(.76,.64,.35)+v*vec3(.19,.15,.13); break;                                        // Sand
    case 16u: c=vec3(.9,.88,.84)+v*.1; break;                                                          // Salt
    case 10u: {float sp=step(.98,hash21(px))*.2;  c=vec3(.19,.18,.17)+v*vec3(.08,.07,.06)+sp; break;} // Gunpowder
    case 17u: c=vec3(.55,.47,.37)+v*vec3(.12,.10,.08); break;                                        // Dust
    case 22u: {float fl=step(.92,hash21(px+f*.1))*.3;float te=clamp(life/120.,0.,1.);
              c=vec3(clamp(.78+fl+v*.06,0,1),.15+te*.31+fl+v*.04,.02+te*.06+v*.02); break;}          // Thermite
    case 23u: {float sh=sin(x*.5+y*.4+f*.12)*.03; c=clamp(vec3(.82,.88,.96)+v*vec3(.1,.1,.04)+sh,0,1); break;} // Snow
    case 24u: c=vec3(.25,.24,.23)+v*vec3(.08,.07,.07); break;                                        // Ash
    case 25u: c=vec3(.18,.14,.10)+v*vec3(.06,.05,.04); break;                                        // Coal
    case 26u: {float sp=step(.97,hash21(px*2.3))*.15; c=vec3(.45,.4,.35)+v*vec3(.1,.09,.08)+sp; break;} // Gravel
    case 27u: c=vec3(.42,.28,.12)+v*vec3(.10,.08,.06); break;                                        // Seed
    case 28u: {float sh=sin(f*.07+x*.3)*.04; c=clamp(vec3(.85,.82,.15)+v*vec3(.12,.10,.08)+sh,0,1); break;} // Sulfur
    /* ---- liquids ---- */
    case  2u: {float sh=sin(x*.4+y*.3+f*.08)*.047; c=clamp(vec3(.07,.39,.76)+v*vec3(.1,.21,.23)+vec3(sh),0,1); break;} // Water
    case  6u: c=vec3(.13,.09,.04)+v*vec3(.10,.06,.04); break;                                        // Oil
    case  7u: {float sh=sin(f*.06+x*.3+y*.2)*.06; c=clamp(vec3(.15,.82,.19)+v*vec3(.12,.17,.12)+vec3(sh),0,1); break;} // Acid
    case  5u: {float sh=sin(f*.04+x*.25+y*.15)*.07;
              c=clamp(vec3(.76,.17,.03)+v*vec3(.23,.29,.07)+vec3(sh,sh*.002,0),0,1); break;}          // Lava
    case 18u: {float w=clamp(life/300.,0.,1.); c=vec3(.19,.12,.06)+v*vec3(.07,.05,.03)+w*vec3(.04,.03,0); break;} // Mud
    case 29u: {float sh=sin(x*.8+y*.6+f*.15)*.06; c=vec3(.65,.67,.72)+sh+v*.08; break;}              // Mercury
    case 30u: {float g=sin(f*.08+x*.2+y*.2)*.04; c=clamp(vec3(.9,.55,.1)+v*vec3(.1,.12,.06)+g,0,1); break;} // Napalm
    case 31u: {float w=sin(x*.3+y*.4+f*.06)*.03; c=vec3(.15,.7,.15)+v*vec3(.08,.15,.08)+vec3(0,w,0); break;} // Slime
    case 32u: {float p=sin(f*.06+x*.4+y*.3)*.08; c=vec3(.08,.35,.08)+v*vec3(.06,.10,.05)+vec3(p,p,0); break;} // Poison
    case 33u: {float g=sin(f*.04+x*.3+y*.2)*.02; c=vec3(.25,.45,.85)+v*vec3(.08,.10,.12)+g; break;}  // Nitro
    case 48u: {float p=clamp(life/500.,0.,1.); c=clamp(vec3(1+v*.05,.5+p*.4+v*.1,.1+p*.2),0,1); break;} // Molten Metal
    /* ---- gases ---- */
    case  3u: {float p=clamp(life/60.,0.,1.); c=vec3(1,.11+p*.82,p*p*.35); break;}                   // Fire
    case  4u: {float p=clamp(life/80.,0.,1.); float g=.15+p*.35; c=vec3(g,g,g+.01); break;}          // Smoke
    case 11u: {float p=clamp(life/70.,0.,1.); float g=.62+p*.23; c=vec3(g-.04,g,g+.03); break;}      // Steam
    case 14u: {float p=sin(f*.05+x*.2+y*.3)*.04; c=clamp(vec3(.82,.82,.58)+v*vec3(.12,.12,.12)+p,0,1); break;} // Gas
    case 21u: {float p=sin(f*.05+x*.4+y*.4)*.06;
              c=clamp(vec3(.55,.11,.66)+v*vec3(.15,.08,.15)+vec3(p,0,p),0,1); break;}                 // Ember
    case 34u: c=vec3(.7,.75,.82)+v*.06; break;                                                         // Hydrogen
    case 35u: {float p=sin(f*.05+x*.25+y*.25)*.08; c=vec3(.15,.08,.25)+v*vec3(.06,.05,.08)+vec3(p,0,p); break;} // Toxic Gas
    case 36u: c=vec3(.55,.72,.92)+v*vec3(.10,.10,.08); break;                                         // Nitrous
    case 37u: {float a=sin(px.x*.15+px.y*.15)*.5+.5; float b=sin(px.x*.15+px.y*.15+2.094)*.5+.5;
              float d=sin(px.x*.15+px.y*.15+4.189)*.5+.5; c=vec3(a,b,d); break;}                     // Confetti
    case 49u: c=vec3(1,clamp(.95+v*.05,0,1),clamp(.7+v*.2,0,1)); break;                               // Spark
    case 50u: c=vec3(.5,.65,.3)+v*vec3(.08,.08,.06); break;                                           // Methane
    /* ---- new liquids ---- */
    case 51u: {float sh=sin(x*.35+y*.35+f*.04)*.04; c=clamp(vec3(.62,.06,.06)+v*vec3(.12,.04,.06)+vec3(sh,0,0),0,1); break;} // Blood
    case 64u: {float sh=sin(f*.03+x*.25+y*.2)*.03; c=clamp(vec3(.82,.68,.18)+v*vec3(.10,.10,.06)+vec3(sh,sh*.5,0),0,1); break;} // Honey
    /* ---- new solids ---- */
    case 52u: {float n2=fract(sin(dot(floor(px*.5),vec2(12.9898,78.233)))*43758.5453);
              c=vec3(.28,.38,.18)+n2*vec3(.08,.10,.05)+v*.06; break;}                               // Lichen
    case 53u: {float sp=step(.96,hash21(px*1.5))*.12; c=vec3(.52,.38,.25)+v*vec3(.08,.06,.06)+sp; break;} // Fungus
    case 54u: {float fl=step(.85,hash21(px+f*.2))*.4; c=vec3(.7,.7,.75)+v*.06+vec3(fl*.3,fl*.3,fl*.25); break;} // Magnesium
    case 55u: c=vec3(.22,.18,.16)+v*vec3(.06,.05,.05); break;                                        // Charcoal
    case 56u: {float sh=sin(x*.3+y*.3+f*.015)*.02; c=clamp(vec3(.58,.42,.18)+v*vec3(.10,.07,.06)+sh,0,1); break;} // Resin
    case 57u: {float mo=step(.5,fract(x*.25))*step(.5,fract(y*.25))*.06;
              c=clamp(vec3(.68,.32,.22)+v*vec3(.08,.05,.04)+mo,0,1); break;}                         // Brick
    case 58u: {float t2=fract(sin(dot(floor(px*.3),vec2(12.9898,78.233)))*43758.5453);
              vec3 pa=vec3(.8,.2,.2),pb=vec3(.2,.6,.8),pc=vec3(.8,.8,.2);
              c=(t2<.33?pa:(t2<.66?pb:pc))+v*.08; break;}                                             // Mosaic
    case 65u: {float sh=sin(x*.4+y*.3)*.02; c=clamp(vec3(.88,.85,.72)+v*vec3(.06,.06,.06)+sh,0,1); break;} // Bone
    /* ---- new gases ---- */
    case 59u: {float ir=sin(f*.12+x*1.5+y*1.5)*.15; c=clamp(vec3(.75,.88,.96)+v*.08+vec3(ir*.15,ir*.1,0),0,1); break;} // Bubble
    case 60u: {float sh=sin(f*.1+x*.5+y*.3)*.06; c=clamp(vec3(.38,.18,.72)+v*vec3(.12,.08,.15)+vec3(sh,0,sh),0,1); break;} // Ozone
    case 61u: {float fl=step(.7,hash21(px+f*.3))*.3; float sh=sin(f*.2+x*.8+y*.6)*.08;
              c=clamp(vec3(.75,.3,1.)+v*vec3(.15,.12,.0)+vec3(sh,sh*.3,sh*.5)+fl,0,1); break;}     // Plasma
    case 62u: {float a2=sin(px.x*.12+px.y*.12+f*.05)*.5+.5; float b2=sin(px.x*.12+px.y*.12+f*.05+2.094)*.5+.5;
              float d2=sin(px.x*.12+px.y*.12+f*.05+4.189)*.5+.5; c=vec3(a2*.9+.1,.15+b2*.3,.2+d2*.5); break;} // Cotton Candy
    /* ---- new liquids ---- */
    case 66u: {float sh=sin(x*.2+y*.2+f*.02)*.02; c=clamp(vec3(.12,.1,.08)+v*vec3(.04,.03,.03)+vec3(sh),0,1); break;} // Tar
    case 74u: {float sh=sin(f*.03+x*.3+y*.3)*.02; c=clamp(vec3(.04,.02,.08)+v*.02+vec3(sh),0,1); break;} // Ink
    /* ---- wave3 solids ---- */
    case 67u: {float yf=clamp(y/u_res.y,.0,1.); c=vec3(.1,.42,.12)+yf*vec3(.08,.18,.04)+v*vec3(.04,.06,.03); break;} // Vine
    case 68u: {float sh=sin(f*.06+x*.5+y*.4)*.04; c=clamp(vec3(.82,.92,.98)+v*vec3(.08,.06,.04)+sh,0,1); break;} // Dry Ice
    case 72u: {float sh=sin(x*.25+y*.25+f*.01)*.015; c=clamp(vec3(.92,.88,.72)+v*vec3(.06,.05,.06)+sh,0,1); break;} // Fat
    case 73u: {float sh=sin(x*.4+y*.3)*.012; float ir=step(.7,fract(sin(dot(floor(px*.3),vec2(12.9898,78.233)))*43758.5453))*.06;
              c=clamp(vec3(.82,.62,.15)+v*vec3(.08,.06,.04)+sh+ir,0,1); break;} // Amber
    case 75u: {float fl=step(.85,hash21(px+f*.15))*.25; float sh=sin(f*.08+x*.6+y*.4)*.04;
              c=clamp(vec3(.25,.82,.25)+v*.08+vec3(fl*.3,0,fl*.15)+vec3(sh,sh,0),0,1); break;} // Radioactive
    case 77u: {float sh=sin(f*.015+x*.4+y*.3)*.02; c=clamp(vec3(.68,.88,.96)+v*vec3(.08,.06,.04)+sh,0,1); break;} // Glacier
    case 79u: {float mo=step(.5,fract(x*.2))*step(.5,fract(y*.15))*.04;
              c=clamp(vec3(.52,.42,.32)+v*vec3(.06,.05,.04)+mo,0,1); break;} // Mudstone
    /* ---- wave3 powders ---- */
    case 70u: {float gl2=step(.8,hash21(px+f*.15))*.35; c=clamp(vec3(.45,.72,.2)+v*vec3(.08,.1,.06)+vec3(gl2*.4,gl2*.35,0),0,1); break;} // Phosphorus
    case 71u: c=vec3(.78,.72,.42)+v*vec3(.1,.08,.06); break; // Grain
    /* ---- wave3 gases ---- */
    case 69u: c=vec3(.52,.52,.52)+v*.06; break; // CO2
    case 76u: {float a3=sin(px.x*.1+px.y*.15+f*.03)*.5+.5; float b3=sin(px.x*.08+px.y*.12+f*.04+1.5)*.5+.5;
              c=clamp(vec3(.92,.9,.85)+a3*.06+b3*.04+v*.03,0,1); break;} // Feather
    case 78u: {float fl2=step(.6,hash21(px+f*.5))*.5; float sh=sin(f*.15+x*1.2+y*1.2)*.1;
              c=clamp(vec3(.4,.6,1.)+v*vec3(.15,.15,.1)+vec3(sh,sh*.5,0)+vec3(fl2*.4,fl2*.4,fl2*.3),0,1); break;} // Electrical
    /* ---- new special ---- */
    case 63u: {float p2=sin(f*.04+x*.4+y*.3)*.06; float swirl=fract(sin(dot(floor(px*.4),vec2(12.9898,78.233)))*43758.5453);
              c=vec3(.04+swirl*.06,.0,.08+swirl*.1)+vec3(p2,0,p2); break;} // Dark Matter
    case 80u: {float fl3=step(.7,hash21(px+f*.4))*.3; float sh=sin(f*.12+x*.9+y*.9)*.08;
              c=clamp(vec3(.15,.0,.4)+v*vec3(.1,.0,.15)+vec3(sh,0,sh*.5)+fl3,0,1); break;} // Antimatter
    /* ---- solids ---- */
    case  8u: c=vec3(.41,.41,.43)+v*.13; break;                                                       // Stone
    case  9u: c=vec3(.39,.23,.10)+v*vec3(.12,.08,.06); break;                                        // Wood
    case 12u: {float s=sin(f*.025+x*.6+y*.4)*.03; c=clamp(vec3(.6,.82,.92)+v*vec3(.12,.10,.06)+s,0,1); break;} // Ice
    case 19u: {float s=sin(f*.02+x*.5+y*.3)*.02; c=clamp(vec3(.62,.78,.86)+v*vec3(.12,.10,.08)+s,0,1); break;} // Glass
    case 13u: {float yf=y/u_res.y; c=vec3(.08,.43,.11)+yf*vec3(.12,.15,.06)+v*vec3(.08,.13,.06); break;} // Plant
    case 38u: {float s=sin(x*.3+y*.2+f*.03)*.02; c=clamp(vec3(.6,.62,.65)+v*vec3(.12,.12,.12)+s,0,1); break;} // Metal
    case 39u: c=vec3(.55,.28,.10)+v*vec3(.10,.08,.05); break;                                        // Rust
    case 40u: c=vec3(.72,.72,.70)+v*.08; break;                                                        // Concrete
    case 41u: c=vec3(.22,.15,.10)+v*vec3(.06,.05,.04); break;                                        // Rubber
    case 42u: {float f2=hash21(px*1.8)*.08; c=vec3(.88,.87,.84)+v*vec3(.08,.08,.08)+f2; break;}       // Cotton
    case 43u: c=vec3(.85,.80,.65)+v*vec3(.08,.07,.06); break;                                         // Wax
    case 44u: {float g=life>0.?clamp(life/250.,0.,1.):0.; c=vec3(.3+g*.6+v*.08,.12+v*.05,.08+v*.04); break;} // Fuse
    case 45u: c=vec3(.50,.50,.52)+v*.08; break;                                                        // Cobweb
    case 46u: {float s=sin(x*.4+y*.3+f*.03)*.016; c=clamp(vec3(.72,.42,.15)+v*vec3(.10,.08,.06)+s,0,1); break;} // Copper
    case 47u: {float st=step(.5,fract(y*.5)); c=clamp(vec3(.75+v*.12+st*.1,.1+v*.05,.1+v*.05),0,1); break;} // Dynamite
    /* ---- special ---- */
    case 15u: {float p=sin(f*.03+x*.5+y*.5)*.03; c=vec3(.08,.02,.16)+vec3(p,0,p); break;}            // Void
    case 20u: c=vec3(.047,.039,.031); break;                                                          // Clone
    default:  c=vec3(.047,.039,.031);                                                                  // Empty / bg
    }
    return c;
}

void main(){
    vec4 d  = texture(u_data, vUv);
    uint t  = uint(d.r * 255.0 + 0.5);   // element type  (0-80)
    float v = d.g;                        // colour variation 0-1
    float life = d.b * 255.0 + d.a * 65280.0;  // reconstruct uint16 life (255*256)

    vec2 px = vUv * u_res;
    vec3 c  = elemColor(t, v, life, px);

    // pseudo-3-D edge darkening
    if(t != 0u){
        vec2 tx = 1.0 / u_res;
        float e = 0.0;
        if(uint(texture(u_data, vUv+vec2(tx.x,0)).r*255.+.5)==0u) e+=.12;
        if(uint(texture(u_data, vUv-vec2(tx.x,0)).r*255.+.5)==0u) e+=.12;
        if(uint(texture(u_data, vUv+vec2(0,tx.y)).r*255.+.5)==0u) e+=.12;
        if(uint(texture(u_data, vUv-vec2(0,tx.y)).r*255.+.5)==0u) e+=.12;
        c *= 1.0 - min(e, 0.35);
    }
    FragColor = vec4(c, 1.0);
}
"""

# --- bloom helpers -----------------------------------------------------
BLOOM_EXTRACT_SRC = """
#version 460 core
in vec2 vUv;
out vec4 FragColor;
uniform sampler2D u_tex;
void main(){
    // 2x2 box down-sample + brightness threshold
    // Offset by 0.5 source texels so NEAREST sampling hits the correct
    // 2x2 block of source texels that map to this half-res fragment.
    vec2 tx = 0.5 / textureSize(u_tex, 0);
    vec3 s = (texture(u_tex, vUv+vec2(-tx.x,-tx.y)).rgb
            + texture(u_tex, vUv+vec2( tx.x,-tx.y)).rgb
            + texture(u_tex, vUv+vec2(-tx.x, tx.y)).rgb
            + texture(u_tex, vUv+vec2( tx.x, tx.y)).rgb) * 0.25;
    float lum = dot(s, vec3(0.2126, 0.7152, 0.0722));
    FragColor = vec4(s * smoothstep(0.18, 0.78, lum), 1.0);
}
"""

# BLUR_SRC removed — replaced by hardware mipmap-based multi-scale bloom (glGenerateMipmap)

COMPOSITE_SRC = """
#version 460 core
in vec2 vUv;
out vec4 FragColor;
uniform sampler2D u_scene;
uniform sampler2D u_bloom;
uniform float u_bloomIntensity;
void main(){
    vec3 base = texture(u_scene, vUv).rgb;

    // Multi-scale bloom from mip levels (replaces 8-pass Gaussian blur).
    // Each mip level doubles the effective blur radius.
    vec3 bloom = vec3(0.0);
    bloom += textureLod(u_bloom, vUv, 1.0).rgb * 0.50;
    bloom += textureLod(u_bloom, vUv, 2.0).rgb * 0.30;
    bloom += textureLod(u_bloom, vUv, 3.0).rgb * 0.20;

    // Vignette on scene only — bloom glow bleeds past darkened edges
    vec2 uv = vUv * 2.0 - 1.0;
    float vig = 1.0 - dot(uv * 0.45, uv * 0.45);
    base *= smoothstep(0.0, 0.7, vig);

    FragColor = vec4(base + bloom * u_bloomIntensity, 1.0);
}
"""

# ================================================================
# SIMULATION — pure data + logic, no Qt or OpenGL dependencies
# ================================================================
class SandSimulation:
    def __init__(self, W=400, H=300):
        self.W, self.H = W, H

        # State Arrays
        self.grid = np.zeros((self.W * self.H), dtype=np.uint8)
        self.color_var = np.zeros((self.W * self.H), dtype=np.uint8)
        self.life = np.zeros((self.W * self.H), dtype=np.uint16)
        self.moved = np.zeros((self.W * self.H), dtype=np.uint32)

        self.frame = 0
        self.selected_type = SAND
        self.brush_size = 4
        self.sim_speed = 1
        self.mouse_down = False
        self.erasing = False
        self.prev_gx, self.prev_gy = -1, -1

        # --- Interaction improvements ---
        # Undo system (stores grid snapshots)
        self._undo_stack = []
        self._undo_limit = 30
        self._stroke_snapshot = None  # snapshot taken at stroke start

        # Speed-adaptive brush density
        self._last_brush_time = time.time()
        self._last_brush_gx = -1
        self._last_brush_gy = -1

        # Shift+click straight line anchor
        self._line_anchor = None  # (gx, gy) or None

        # Python optimization: Cache random function locally
        self.r = random.random
        self.ri = random.randint
        self._shuf_buf = list(self._NBR8)

    def idx(self, x, y): return y * self.W + x
    def in_b(self, x, y): return 0 <= x < self.W and 0 <= y < self.H
    def get(self, x, y): return self.grid[y * self.W + x] if self.in_b(x, y) else -1
    def is_empty(self, x, y): return self.get(x, y) == EMPTY

    # Pre-computed neighbor offsets (8-connected)
    _NBR8 = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))

    # Type-category checks (frozenset for O(1) lookup, no tuple alloc per call)
    _LIQUIDS = frozenset((WATER, OIL, ACID, MERCURY, NAPALM, SLIME, POISON, NITRO, BLOOD, HONEY, TAR, INK))
    _MERCURY_SINK = _LIQUIDS - frozenset((MERCURY,)) | frozenset((MOLTEN_METAL,))
    _GASES = frozenset((SMOKE, STEAM, GAS, HYDROGEN, TOXIC_GAS, NITROUS, METHANE, BUBBLE, OZONE, PLASMA, COTTON_CANDY, CO2, FEATHER, ELECTRICAL))
    _HEAT_SOURCES = frozenset((FIRE, LAVA, EMBER, SPARK, PLASMA))
    _COOL_SOURCES = frozenset((ICE, DRY_ICE, GLACIER))

    def is_liq(self, t): return t in self._LIQUIDS
    def is_gas(self, t): return t in self._GASES

    # Life initialization ranges for elements that use life: type -> (lo, hi)
    _LIFE_INIT = {
        FIRE: (35, 80), SMOKE: (50, 120), LAVA: (400, 700), STEAM: (60, 110),
        EMBER: (80, 140), MUD: (250, 500), ASH: (200, 400), HYDROGEN: (40, 80),
        TOXIC_GAS: (80, 160), NITROUS: (60, 100), CONFETTI: (120, 250),
        RUST: (300, 600), SPARK: (8, 20), MOLTEN_METAL: (200, 500), METHANE: (80, 150),
        FUNGUS: (500, 1000), CHARCOAL: (80, 160), BUBBLE: (30, 80),
        OZONE: (60, 120), PLASMA: (20, 50), COTTON_CANDY: (80, 160),
        DARK_MATTER: (600, 1200),
        CO2: (60, 120), FEATHER: (120, 250), ELECTRICAL: (15, 35),
        RADIOACTIVE: (800, 1500), ANTIMATTER: (200, 400),
    }

    # Neighbor types that poison/toxic_gas destroy (organic matter)
    _ORGANICS = frozenset((PLANT, WOOD, COTTON, SEED, LICHEN, FUNGUS, BONE, VINE, FAT, GRAIN))

    # ================================================================
    # DATA-DRIVEN REACTION TABLES
    # ================================================================
    # Shared lookup tables used by multiple hot elements.
    # _react_heat() consolidates ~200 lines of duplicated elif chains
    # across fire, ember, lava, molten_metal, and spark into one call.
    #
    # prob_mult: scales base probabilities per-caller (fire=1.3, ember/lava=0.8, molten=0.5, spark=2.0)
    # allow_explode_prob: True for elements that can trigger probabilistic explosions

    # Elements that immediately explode on contact with heat sources
    EXPLODE_ON_HEAT = {
        NITRO: 10, DYNAMITE: 8, HYDROGEN: 5, METHANE: 7, GAS: 4, GUNPOWDER: 3,
        BUBBLE: 2,
    }

    # Chain-reaction elements in explode(): element -> explosion radius
    EXPLODE_CHAIN = {
        NITRO: 10, DYNAMITE: 8, HYDROGEN: 5, METHANE: 7, SULFUR: 3, NITROUS: 3,
        BUBBLE: 2, OZONE: 2,
    }
    # Elements that explode() converts to fire (not chain, not clear)
    EXPLODE_IGNITES = frozenset((OIL, NAPALM, GUNPOWDER, GAS, DUST, HONEY, BLOOD, TAR, FAT, INK))
    # Elements that explode with a probability check (used by lava/molten which are "hotter" but slower)
    EXPLODE_ON_HEAT_PROB = {
        DUST: (6, 0.15), SULFUR: (3, 0.15), NITROUS: (3, 0.1),
    }

    # Elements that ignite when touched by heat.
    # Format: (probability, result_type, extra_data)
    #   result_type: 'FIRE' (default), 'SMOKE', 'OIL', 'FUSE'
    #   For FIRE:  extra_data = (life_lo, life_hi) or None for default
    #   For FUSE: extra_data = (timer_lo, timer_hi)
    #   For SMOKE/OIL: extra_data = None
    IGNITE_ON_HEAT = {
        OIL:          (0.25,  'FIRE',  (35, 80)),
        WOOD:         (0.025, 'FIRE',  (60, 110)),
        PLANT:        (0.04,  'FIRE',  (45, 85)),
        COTTON:       (0.15,  'FIRE',  (30, 60)),
        NAPALM:       (0.15,  'FIRE',  (100, 160)),
        COBWEB:       (0.1,   'SMOKE', None),
        SLIME:        (0.03,  'FIRE',  (35, 80)),
        WAX:          (0.06,  'OIL',   None),
        RUBBER:       (0.05,  'OIL',   None),
        FUSE:         (0.15,  'FUSE',  (150, 250)),
        FUNGUS:       (0.06,  'FIRE',  (35, 60)),
        BLOOD:        (0.02,  'FIRE',  (20, 40)),
        HONEY:        (0.04,  'FIRE',  (50, 90)),
        CHARCOAL:     (0.008, 'FIRE',  (100, 180)),
        LICHEN:       (0.015, 'FIRE',  (25, 45)),
        RESIN:        (0.05,  'OIL',   None),
        BONE:         (0.008, 'FIRE',  (20, 40)),
        COTTON_CANDY: (0.2,   'FIRE',  (25, 50)),
        TAR:          (0.02,  'FIRE',  (80, 140)),
        FAT:          (0.06,  'OIL',   None),
        VINE:         (0.03,  'FIRE',  (30, 60)),
        FEATHER:      (0.15,  'FIRE',  (20, 40)),
        AMBER:        (0.04,  'OIL',   None),
        INK:          (0.01,  'FIRE',  (25, 50)),
    }

    # Elements that convert to something special (not just FIRE)
    CONVERT_ON_HEAT = {
        ICE: ('WATER', 0.15), SNOW: ('WATER', 0.2),
        COAL: ('FIRE_LIFE', 80, 130),  # fire with longer life
        MERCURY: ('TOXIC_GAS', 0.02),
        SALT: ('GLASS', 0.005),
    }

    # Acid dissolve rates: element → (rate, result_type)
    # result_type: None = clear, or element ID to convert to
    ACID_RATES = {
        METAL: (0.001, None), CONCRETE: (0.0005, None),
        COBWEB: (0.03, None), COTTON: (0.02, SMOKE),
        WOOD: (0.012, None), GLASS: (0.004, None),
        GRAVEL: (0.003, None), RUST: (0.008, None),
        COPPER: (0.006, TOXIC_GAS), SLIME: (0.015, None),
        BONE: (0.01, None), LICHEN: (0.015, None), FUNGUS: (0.012, TOXIC_GAS),
        BRICK: (0.0003, None), CHARCOAL: (0.004, None), RESIN: (0.008, None),
        MOSAIC: (0.001, None), MAGNESIUM: (0.006, HYDROGEN),
        VINE: (0.01, None), FAT: (0.015, OIL), AMBER: (0.0005, None),
        RADIOACTIVE: (0.003, TOXIC_GAS), MUDSTONE: (0.002, MUD), GLACIER: (0.0002, None),
        DRY_ICE: (0.02, CO2), PHOSPHORUS: (0.008, SMOKE), GRAIN: (0.01, None),
    }
    ACID_SKIP = frozenset((EMPTY, ACID, LAVA, STONE, VOID_E, RUBBER, DARK_MATTER, ANTIMATTER, GLACIER, CO2))
    # Default acid rate for elements not in ACID_RATES
    ACID_DEFAULT_RATE = 0.04

    # Water/ice quench reactions for heat sources
    # (element_type, neighbor_type) → (result_on_self, result_on_neighbor)
    _QUENCH_TABLE = {
        (FIRE, WATER): (SMOKE, SMOKE),
        (LAVA, WATER): (SMOKE, SMOKE),
        (EMBER, WATER): (STEAM, STEAM),
        (PLASMA, WATER): (STEAM, STEAM),
        (MOLTEN_METAL, WATER): (METAL, STEAM),
        (MOLTEN_METAL, ICE): (METAL, STEAM),
    }

    def _check_quench(self, x, y, nx, ny, n, self_type):
        """Check if neighbor quenches this element (water/ice). Returns True if quenched."""
        q = self._QUENCH_TABLE.get((self_type, n))
        if not q: return False
        self.set_cell(x, y, q[0]); self.set_cell(nx, ny, q[1]); return True

    # Helper: process neighbor reactions for heat sources (fire/ember/lava/molten/spark/plasma)
    def _react_heat(self, nx, ny, n, prob_mult=1.0, allow_explode_prob=False):
        """Try heat-based reaction on neighbor. Returns True if reacted."""
        # 1) Immediate explosions
        if n in self.EXPLODE_ON_HEAT:
            self.explode(nx, ny, self.EXPLODE_ON_HEAT[n]); return True
        # 2) Probabilistic explosions
        if allow_explode_prob and n in self.EXPLODE_ON_HEAT_PROB:
            radius, prob = self.EXPLODE_ON_HEAT_PROB[n]
            if self.r() < prob * prob_mult:
                self.explode(nx, ny, radius); return True
        # 3) Ignitions (data-driven: each entry has result_type + extra_data)
        if n in self.IGNITE_ON_HEAT:
            prob, result_type, extra = self.IGNITE_ON_HEAT[n]
            if self.r() < prob * prob_mult:
                if result_type == 'SMOKE':
                    self.set_cell(nx, ny, SMOKE)
                elif result_type == 'OIL':
                    self.set_cell(nx, ny, OIL)
                elif result_type == 'FUSE':
                    lo, hi = extra
                    self.life[self.idx(nx, ny)] = self.ri(lo, hi)
                else:  # 'FIRE'
                    self.set_cell(nx, ny, FIRE)
                    if extra:
                        lo, hi = extra
                        self.life[self.idx(nx, ny)] = self.ri(lo, hi)
                return True
        # 4) Conversions
        if n in self.CONVERT_ON_HEAT:
            entry = self.CONVERT_ON_HEAT[n]
            if entry[0] == 'FIRE_LIFE':
                _, lo, hi = entry
                if self.r() < 0.008 * prob_mult:
                    self.set_cell(nx, ny, FIRE)
                    self.life[self.idx(nx, ny)] = self.ri(lo, hi)
                    return True
            else:
                result_name, prob = entry[0], entry[1]
                result = {'WATER': WATER, 'TOXIC_GAS': TOXIC_GAS, 'GLASS': GLASS}[result_name]
                if self.r() < prob * prob_mult:
                    self.set_cell(nx, ny, result); return True
        return False

    # Acid helper using data table
    def _react_acid(self, nx, ny, n):
        """Try acid reaction on neighbor. Returns True if reacted."""
        rate, result = self.ACID_RATES.get(n, (self.ACID_DEFAULT_RATE, None))
        if self.r() < rate:
            if result is not None:
                self.set_cell(nx, ny, result)
            else:
                self.clear_cell(nx, ny)
            return True
        return False

    # Cold reaction table: element → (cold_source_prob, result_type)
    # Used by ICE, DRY_ICE, GLACIER
    _COLD_FREEZE = {
        WATER: (0.008, ICE),
        MUD: (0.005, ICE),
        SLIME: (0.005, ICE),
        BLOOD: (0.005, ICE),
        HONEY: (0.005, ICE),
        TAR: (0.003, ICE),
        INK: (0.003, ICE),
    }
    _COLD_SOLIDIFY = {
        LAVA: (0.02, STONE),
        FIRE: (0.08, STEAM),
        EMBER: (0.05, ASH),
        PLASMA: (0.05, STEAM),
        STEAM: (0.01, WATER),
    }

    def _react_cold(self, nx, ny, n, prob_mult=1.0):
        """Try cold-based reaction on neighbor. Returns True if reacted."""
        if n in self._COLD_FREEZE:
            prob, result = self._COLD_FREEZE[n]
            if self.r() < prob * prob_mult:
                self.set_cell(nx, ny, result); return True
        if n in self._COLD_SOLIDIFY:
            prob, result = self._COLD_SOLIDIFY[n]
            if self.r() < prob * prob_mult:
                self.set_cell(nx, ny, result); return True
        return False

    def gas_move(self, x, y, rise_prob=0.65, side_prob=0.3):
        """Shared gas movement logic: rise, diagonal rise, then sideways.
        Returns True if the gas moved, False otherwise.
        Gases can swap with other gas types to prevent unnatural stacking."""
        if self.r() < rise_prob:
            if self.is_empty(x, y-1):
                self.move_cell(x, y, x, y-1); return True
            # Swap with another gas above (lighter gases push through heavier ones)
            above = self.get(x, y-1)
            if self.is_gas(above) and above != self.grid[self.idx(x,y)]:
                self.swap_cells(x, y, x, y-1); return True
            d = -1 if self.r() < 0.5 else 1
            for dd in (d, -d):
                nx, ny = x+dd, y-1
                if self.is_empty(nx, ny):
                    self.move_cell(x, y, nx, ny); return True
                n = self.get(nx, ny)
                if self.is_gas(n) and n != self.grid[self.idx(x,y)]:
                    self.swap_cells(x, y, nx, ny); return True
        if self.r() < side_prob:
            d = -1 if self.r() < 0.5 else 1
            for dd in (d, -d):
                if self.is_empty(x+dd, y):
                    self.move_cell(x, y, x+dd, y); return True
        return False
    def dec_life(self, i, amt=1):
        """Safely decrement uint16 life, returns new value (never wraps below 0)."""
        v = int(self.life[i]) - amt
        if v < 0: v = 0
        self.life[i] = v
        return v

    # ---- Neighbor helpers (reduce boilerplate in update methods) ----

    def _any_neighbor_in(self, x, y, types):
        """Return True if any 8-neighbor is in *types* (frozenset/tuple/set)."""
        get = self.get
        for dx, dy in self._NBR8:
            if get(x+dx, y+dy) in types:
                return True
        return False

    def _find_neighbor(self, x, y, types):
        """Return (nx, ny, type) of first neighbor matching *types*, or None."""
        get = self.get
        for dx, dy in self._NBR8:
            n = get(x+dx, y+dy)
            if n in types:
                return (x+dx, y+dy, n)
        return None

    def _find_all_neighbors(self, x, y, types):
        """Return list of (nx, ny, type) for all neighbors matching *types*."""
        get = self.get
        result = []
        for dx, dy in self._NBR8:
            n = get(x+dx, y+dy)
            if n in types:
                result.append((x+dx, y+dy, n))
        return result

    def _shuffled_dirs(self):
        """Shuffle and return _shuf_buf (reusable pre-allocated list)."""
        random.shuffle(self._shuf_buf)
        return self._shuf_buf

    # Powders tuple — shared by cobweb, resin, honey, tar, fat
    _POWDERS = (SAND, SALT, DUST, ASH, SNOW, COAL, GRAVEL, SEED, SULFUR,
                GUNPOWDER, THERMITE, CHARCOAL, CONFETTI, PHOSPHORUS, GRAIN)

    def _catch_powders(self, x, y, prob, directions=None):
        """Sticky/viscous elements: pin powders above them so they don't fall through.
        directions: which relative positions to check (default: above + diagonals above)."""
        if self.r() >= prob: return
        if directions is None:
            directions = ((0,-1),(-1,-1),(1,-1))
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if self.get(nx, ny) in self._POWDERS:
                if self.r() < 0.5:
                    self.moved[self.idx(nx, ny)] = self.frame

    def set_cell(self, x, y, t):
        if not self.in_b(x, y): return
        i = self.idx(x, y)
        self.grid[i] = t; self.moved[i] = self.frame
        # CLONE and VOID should have zero variation (visual consistency)
        if t in (CLONE, VOID_E, CONCRETE, STONE, GLASS, METAL, COPPER, RUST, BRICK, MOSAIC, BONE, GLACIER, MUDSTONE, AMBER):
            self.color_var[i] = 0
        else:
            self.color_var[i] = self.ri(0, 255)
        init = self._LIFE_INIT.get(t)
        self.life[i] = self.ri(init[0], init[1]) if init else 0

    def clear_cell(self, x, y):
        if not self.in_b(x, y): return
        i = self.idx(x, y); self.grid[i] = EMPTY; self.color_var[i] = 0; self.life[i] = 0

    def move_cell(self, x1, y1, x2, y2):
        if not self.in_b(x2, y2): return
        a, b = self.idx(x1, y1), self.idx(x2, y2)
        self.grid[b]=self.grid[a]; self.color_var[b]=self.color_var[a]; self.life[b]=self.life[a]; self.moved[b]=self.frame
        self.grid[a]=EMPTY; self.color_var[a]=0; self.life[a]=0

    def swap_cells(self, x1, y1, x2, y2):
        if not self.in_b(x2, y2): return
        a, b = self.idx(x1, y1), self.idx(x2, y2)
        for arr in (self.grid, self.color_var, self.life): arr[a], arr[b] = arr[b], arr[a]
        self.moved[a] = self.frame; self.moved[b] = self.frame

    def explode(self, cx, cy, r):
        queue = deque([(cx, cy, r)])
        chain = self.EXPLODE_CHAIN
        ignites = self.EXPLODE_IGNITES
        skip = (STONE, VOID_E, METAL, CONCRETE, BRICK, DARK_MATTER, GLACIER, ANTIMATTER)
        while queue:
            cx, cy, r = queue.popleft()
            for dy in range(-r, r+1):
                for dx in range(-r, r+1):
                    if dx*dx + dy*dy > r*r: continue
                    nx, ny = cx+dx, cy+dy
                    if not self.in_b(nx, ny): continue
                    n = self.get(nx, ny)
                    if n in skip: continue
                    if n == GLASS: self.clear_cell(nx, ny); continue
                    if n in chain:
                        self.clear_cell(nx, ny); queue.append((nx, ny, chain[n])); continue
                    if n == MERCURY: self.set_cell(nx, ny, TOXIC_GAS); continue
                    if n in ignites:
                        self.set_cell(nx, ny, FIRE); continue
                    if n == THERMITE: self.set_cell(nx, ny, EMBER); self.life[self.idx(nx,ny)]=100; continue
                    if n != EMPTY: self.clear_cell(nx, ny)
            for dy in range(-r-1, r+2):
                for dx in range(-r-1, r+2):
                    d2 = dx*dx + dy*dy
                    if d2 <= r*r or d2 > (r+1)*(r+1): continue
                    if self.is_empty(cx+dx, cy+dy) and self.r() < 0.5: self.set_cell(cx+dx, cy+dy, FIRE)

    def fall_pow(self, x, y):
        b = self.get(x, y+1)
        if b == EMPTY: self.move_cell(x, y, x, y+1); return
        if self.is_liq(b): self.swap_cells(x, y, x, y+1); return
        d = -1 if self.r() < 0.5 else 1
        bl, br = self.get(x+d, y+1), self.get(x-d, y+1)
        if bl == EMPTY: self.move_cell(x, y, x+d, y+1); return
        if self.is_liq(bl): self.swap_cells(x, y, x+d, y+1); return
        if br == EMPTY: self.move_cell(x, y, x-d, y+1); return
        if self.is_liq(br): self.swap_cells(x, y, x-d, y+1); return

    def liquid_move(self, x, y, sink_through=None, fall_prob=1.0, spread_prob=1.0, diag_prob=1.0, sink_all_liq=False, spread_independent=False):
        """Shared liquid movement: fall, diagonal fall, sideways spread.
        sink_through: set of element types to swap-with when below (e.g. {WATER} for oil).
        sink_all_liq: if True, sink through any liquid below/diagonal (for heavy liquids like lava).
        spread_independent: if True, sideways spread runs even when fall section is skipped."""
        did_fall_section = False
        if self.r() < fall_prob:
            did_fall_section = True
            b = self.get(x, y+1)
            if b == EMPTY:
                self.move_cell(x, y, x, y+1); return True
            if sink_through and b in sink_through:
                self.swap_cells(x, y, x, y+1); return True
            if sink_all_liq and self.is_liq(b):
                self.swap_cells(x, y, x, y+1); return True
            d = -1 if self.r() < 0.5 else 1
            # Diagonal fall
            if self.r() < diag_prob:
                bl = self.get(x+d, y+1)
                if bl == EMPTY: self.move_cell(x, y, x+d, y+1); return True
                if sink_all_liq and self.is_liq(bl):
                    self.swap_cells(x, y, x+d, y+1); return True
                br = self.get(x-d, y+1)
                if br == EMPTY: self.move_cell(x, y, x-d, y+1); return True
                if sink_all_liq and self.is_liq(br):
                    self.swap_cells(x, y, x-d, y+1); return True
        # Sideways spread (independent of fall if spread_independent=True)
        if spread_independent or did_fall_section:
            if self.r() < spread_prob:
                d = -1 if self.r() < 0.5 else 1
                if self.is_empty(x+d, y): self.move_cell(x, y, x+d, y); return True
                if self.is_empty(x-d, y): self.move_cell(x, y, x-d, y); return True
        return False

    # ---- Existing element updates (with new interactions) ----

    # ---- Heat source movement helpers (shared by fire, ember, spark) ----

    def _heat_source_move(self, x, y, pattern):
        """Movement patterns for heat-source elements.
        pattern: 'fire' (rise + diagonal rise + sideways),
                 'ember' (mostly fall, rarely rise),
                 'spark' (random 8-dir), handled by caller.
        Returns True if moved."""
        if pattern == 'fire':
            if self.is_empty(x, y-1): self.move_cell(x, y, x, y-1); return True
            above = self.get(x, y-1)
            if self.is_gas(above): self.swap_cells(x, y, x, y-1); return True
            d = -1 if self.r() < 0.5 else 1
            if self.is_empty(x+d, y-1): self.move_cell(x, y, x+d, y-1); return True
            if self.is_empty(x-d, y-1): self.move_cell(x, y, x-d, y-1); return True
            if self.r() < 0.4:
                if self.is_empty(x+d, y): self.move_cell(x, y, x+d, y); return True
                if self.is_empty(x-d, y): self.move_cell(x, y, x-d, y); return True
        return False

    def update_sand(self, x, y):
        if self.r() < 0.006:
            for dx2, dy2 in self._NBR8:
                if self.get(x+dx2, y+dy2) in self._HEAT_SOURCES and self.r() < 0.4:
                    self.set_cell(x, y, GLASS); return
        self.fall_pow(x, y)

    def update_water(self, x, y):
        if self.r() < 0.004:
            for dx2, dy2 in self._NBR8:
                n = self.get(x+dx2, y+dy2)
                if n == SAND: self.set_cell(x, y, MUD); return
                if n == HONEY and self.r() < 0.3: self.set_cell(x, y, SLIME); return
        self.liquid_move(x, y, sink_through={OIL})

    def update_fire(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0:
            rv = self.r()
            if rv < 0.12: self.set_cell(x, y, EMBER)
            elif rv < 0.42: self.set_cell(x, y, SMOKE)
            else: self.clear_cell(x, y)
            return
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                nx, ny, n = x+dx, y+dy, self.get(x+dx, y+dy)
                # Fire-specific: water extinguishes (mutual destruction)
                if self._check_quench(x, y, nx, ny, n, FIRE): return
                # Fire-specific: glass shatters
                if n == GLASS and self.r() < 0.02: self.clear_cell(nx, ny)
                # DUST is immediate for fire (not prob-based like lava)
                if n == DUST: self.explode(nx, ny, 6); return
                # SULFUR is immediate for fire
                if n == SULFUR: self.explode(nx, ny, 3); return
                # Use shared heat reaction table
                if self._react_heat(nx, ny, n, prob_mult=1.3, allow_explode_prob=True):
                    return
        self._heat_source_move(x, y, 'fire'); return

    def update_smoke(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        self.gas_move(x, y, rise_prob=0.55, side_prob=0.25)

    def update_lava(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0:
            if self.r() < 0.15: self.set_cell(x, y, EMBER)
            else: self.set_cell(x, y, STONE)
            return
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                nx, ny, n = x+dx, y+dy, self.get(x+dx, y+dy)
                # Lava-specific: water → smoke (mutual)
                if self._check_quench(x, y, nx, ny, n, LAVA): return
                # Lava-specific: SAND/SALT → glass, MUD → sand
                if n == SAND and self.r() < 0.005: self.set_cell(nx, ny, GLASS); return
                if n == SALT and self.r() < 0.005: self.set_cell(nx, ny, GLASS); return
                if n == MUD and self.r() < 0.03: self.set_cell(nx, ny, SAND); return
                # Lava-specific: metal → molten metal
                if n == METAL and self.r() < 0.004: self.set_cell(nx, ny, MOLTEN_METAL); return
                # Lava-specific: mercury → toxic gas (higher rate than fire)
                if n == MERCURY and self.r() < 0.04: self.set_cell(nx, ny, TOXIC_GAS); return
                # Use shared heat reaction table
                if self._react_heat(nx, ny, n, prob_mult=0.8, allow_explode_prob=True):
                    return
        self.liquid_move(x, y, fall_prob=0.25, spread_prob=0.0, sink_all_liq=True)

    def update_oil(self, x, y):
        self.liquid_move(x, y, sink_through={WATER})

    def update_acid(self, x, y):
        reacted = False
        for dx2, dy2 in self._NBR8:
            nx, ny, n = x+dx2, y+dy2, self.get(x+dx2, y+dy2)
            if n <= 0 or n in self.ACID_SKIP: continue
            if self._react_acid(nx, ny, n):
                reacted = True
        if reacted and self.r() < 0.15:
            if self.is_empty(x, y-1) and self.r() < 0.4: self.set_cell(x, y-1, SMOKE)
            self.clear_cell(x, y); return
        self.liquid_move(x, y, sink_through={OIL})

    def update_wood(self, x, y):
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES) and self.r() < 0.018:
            self.set_cell(x, y, FIRE); self.life[self.idx(x,y)] = self.ri(60, 110)

    def update_gunpowder(self, x, y):
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES):
            self.explode(x, y, 3); return
        self.fall_pow(x, y)

    def update_steam(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0:
            if self.r() < 0.3: self.set_cell(x, y, WATER)
            else: self.clear_cell(x, y)
            return
        self.gas_move(x, y, rise_prob=0.75, side_prob=0.3)

    def update_ice(self, x, y):
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES) and self.r() < 0.12:
            self.set_cell(x, y, WATER); return
        # Ice's cold aura: freeze adjacent liquids slowly
        if self.r() < 0.002:
            for dx2, dy2 in self._NBR8:
                if self._react_cold(x+dx2, y+dy2, self.get(x+dx2, y+dy2), prob_mult=0.25):
                    return

    def update_plant(self, x, y):
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES) and self.r() < 0.035:
            self.set_cell(x, y, FIRE); self.life[self.idx(x,y)] = self.ri(45, 85); return
        waters = self._find_all_neighbors(x, y, (WATER,))
        if waters and self.r() < 0.006:
            wx, wy, _ = waters[self.ri(0, len(waters) - 1)]
            dirs = [(0,-1),(-1,-1),(1,-1),(-1,0),(1,0),(0,1)]
            d = dirs[self.ri(0, len(dirs) - 1)]
            if self.is_empty(x+d[0], y+d[1]):
                self.set_cell(x+d[0], y+d[1], PLANT); self.clear_cell(wx, wy)

    def update_gas(self, x, y):
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES): self.explode(x, y, 4); return
        self.gas_move(x, y, rise_prob=0.65, side_prob=0.4)

    def update_void(self, x, y):
        for k in range(2):
            dx, dy = self._shuffled_dirs()[k]
            nx, ny = x+dx, y+dy
            n = self.get(nx, ny)
            if n > 0 and n != VOID_E: self.clear_cell(nx, ny)

    def update_salt(self, x, y):
        for dx2, dy2 in self._NBR8:
            n = self.get(x+dx2, y+dy2)
            if n == WATER and self.r() < 0.025: self.clear_cell(x, y); return
            if n == ICE and self.r() < 0.05: self.set_cell(x+dx2, y+dy2, WATER); self.clear_cell(x, y); return
        self.liquid_move(x, y, sink_through={WATER}, fall_prob=0.7)

    def update_dust(self, x, y):
        for dx2, dy2 in self._NBR8:
            if self.get(x+dx2, y+dy2) in self._HEAT_SOURCES and self.r() < 0.5: self.explode(x, y, 6); return
        if self.r() < 0.5: self.fall_pow(x, y)

    def update_mud(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.set_cell(x, y, SAND); return
        if self.r() < 0.3:
            if self.liquid_move(x, y, fall_prob=0.3):
                return
        if self.r() < 0.08:
            d = -1 if self.r() < 0.5 else 1
            if self.is_empty(x+d, y): self.move_cell(x, y, x+d, y)

    def update_glass(self, x, y):
        for dx2, dy2 in self._NBR8:
            n = self.get(x+dx2, y+dy2)
            if n == FIRE and self.r() < 0.025: self.clear_cell(x, y); return
            if n == THERMITE and self.r() < 0.5: self.clear_cell(x, y); return
            if n == PLASMA and self.r() < 0.005: self.clear_cell(x, y); return

    def update_clone(self, x, y):
        if self.r() > 0.35: return
        _skip = (CLONE, GLASS, STONE, VOID_E)
        source = -1
        for dx, dy in self._shuffled_dirs():
            b = self.get(x+dx, y+dy)
            if b > 0 and b not in _skip:
                source = b; break
        if source < 0: return
        for pdx, pdy in [(0,-1),(-1,-1),(1,-1),(-1,0),(1,0),(0,1)]:
            if self.is_empty(x+pdx, y+pdy): self.set_cell(x+pdx, y+pdy, source); return

    def update_ember(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0:
            if self.r() < 0.2: self.set_cell(x, y, SMOKE)
            else: self.clear_cell(x, y)
            return
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                nx, ny, n = x+dx, y+dy, self.get(x+dx, y+dy)
                # Ember-specific: water → steam (both cells)
                if self._check_quench(x, y, nx, ny, n, EMBER): return
                # Ember-specific: DUST/SULFUR immediate explode
                if n == DUST: self.explode(nx, ny, 6); return
                if n == SULFUR and self.r() < 0.1: self.explode(nx, ny, 3); return
                # Use shared heat reaction table
                if self._react_heat(nx, ny, n, prob_mult=0.8, allow_explode_prob=True):
                    return
        if self.r() < 0.4:
            if self.is_empty(x, y+1): self.move_cell(x, y, x, y+1); return
            d = -1 if self.r() < 0.5 else 1
            if self.is_empty(x+d, y+1): self.move_cell(x, y, x+d, y+1); return
        if self.r() < 0.12:
            if self.is_empty(x, y-1): self.move_cell(x, y, x, y-1); return
            # Swap with gases above so ember isn't trapped
            if self.is_gas(self.get(x, y-1)):
                self.swap_cells(x, y, x, y-1); return

    def update_thermite(self, x, y):
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                n = self.get(x+dx, y+dy)
                if n == FIRE or n == LAVA or n == EMBER or n == PLASMA:
                    self.set_cell(x, y, EMBER); self.life[self.idx(x,y)] = 120
                    for ddy in (-1,0,1):
                        for ddx in (-1,0,1):
                            if ddx==0 and ddy==0: continue
                            nn = self.get(x+ddx, y+ddy)
                            if nn <= 0 or nn == THERMITE or nn == VOID_E or nn == CLONE: continue
                            if nn == STONE or nn == GLASS or nn == METAL or nn == CONCRETE:
                                self.clear_cell(x+ddx, y+ddy)
                                if self.r() < 0.25 and self.is_empty(x+ddx, y-1): self.set_cell(x+ddx, y-1, EMBER)
                            elif nn == WATER: self.set_cell(x+ddx, y+ddy, STEAM)
                            elif nn == ICE: self.set_cell(x+ddx, y+ddy, WATER)
                            elif nn == SAND and self.r() < 0.35: self.set_cell(x+ddx, y+ddy, GLASS)
                            elif self.r() < 0.55: self.set_cell(x+ddx, y+ddy, EMBER)
                            else: self.set_cell(x+ddx, y+ddy, FIRE)
                    return
        self.fall_pow(x, y)

    # ---- New element updates (IDs 23-50) ----

    def update_snow(self, x, y):
        for dx2, dy2 in self._NBR8:
            n = self.get(x+dx2, y+dy2)
            if n in self._HEAT_SOURCES and self.r() < 0.15: self.set_cell(x, y, WATER); return
            if n == WATER and self.r() < 0.002: self.set_cell(x, y, WATER); return
        if self.r() < 0.5: self.fall_pow(x, y)

    def update_ash(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        if self.r() < 0.3: self.fall_pow(x, y)

    def update_coal(self, x, y):
        for dx2, dy2 in self._NBR8:
            if self.get(x+dx2, y+dy2) in self._HEAT_SOURCES and self.r() < 0.008:
                self.set_cell(x, y, FIRE); self.life[self.idx(x,y)] = self.ri(80, 130); return
        self.fall_pow(x, y)

    def update_gravel(self, x, y):
        self.fall_pow(x, y)

    def update_seed(self, x, y):
        for dx2, dy2 in self._NBR8:
            n = self.get(x+dx2, y+dy2)
            if n in (WATER, MUD) and self.r() < 0.02:
                self.set_cell(x, y, PLANT); self.clear_cell(x+dx2, y+dy2); return
        self.fall_pow(x, y)

    def update_sulfur(self, x, y):
        for dx2, dy2 in self._NBR8:
            if self.get(x+dx2, y+dy2) in self._HEAT_SOURCES and self.r() < 0.15:
                self.explode(x, y, 3); return
        self.fall_pow(x, y)

    def update_mercury(self, x, y):
        for dx2, dy2 in self._NBR8:
            n = self.get(x+dx2, y+dy2)
            if n == ACID and self.r() < 0.02:
                self.set_cell(x+dx2, y+dy2, TOXIC_GAS); self.clear_cell(x, y); return
        self.liquid_move(x, y, sink_through=self._MERCURY_SINK, spread_prob=0.3)

    def update_napalm(self, x, y):
        for dx2, dy2 in self._NBR8:
            nx, ny, n = x+dx2, y+dy2, self.get(x+dx2, y+dy2)
            if n in self._HEAT_SOURCES and self.r() < 0.1:
                self.set_cell(x, y, FIRE); self.life[self.idx(x,y)] = self.ri(100, 160); return
            if n in (WOOD, PLANT, COTTON) and self.r() < 0.03: self.set_cell(nx, ny, FIRE); return
        self.liquid_move(x, y, sink_through={WATER, OIL})

    def update_slime(self, x, y):
        self.liquid_move(x, y, fall_prob=0.15, spread_prob=0.08, sink_all_liq=True, spread_independent=True)

    def update_poison(self, x, y):
        for dx2, dy2 in self._NBR8:
            n = self.get(x+dx2, y+dy2)
            if n in self._ORGANICS and self.r() < 0.08: self.set_cell(x+dx2, y+dy2, TOXIC_GAS); return
        self.liquid_move(x, y, sink_through={OIL})

    def update_nitro(self, x, y):
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES): self.explode(x, y, 10); return
        self.liquid_move(x, y)

    def update_hydrogen(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES): self.explode(x, y, 5); return
        self.gas_move(x, y, rise_prob=0.9, side_prob=0.5)

    def update_toxic_gas(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        for dx2, dy2 in self._NBR8:
            n = self.get(x+dx2, y+dy2)
            if n in self._ORGANICS and self.r() < 0.05: self.set_cell(x+dx2, y+dy2, TOXIC_GAS); return
        # Toxic gas is heavier — rises slowly, sometimes sinks
        if self.r() < 0.1 and self.is_empty(x, y+1):
            self.move_cell(x, y, x, y+1); return
        self.gas_move(x, y, rise_prob=0.25, side_prob=0.2)

    def update_nitrous(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        for dx2, dy2 in self._NBR8:
            if self.get(x+dx2, y+dy2) in self._HEAT_SOURCES:
                self.explode(x, y, 3); return
        self.gas_move(x, y, rise_prob=0.65, side_prob=0.3)

    def update_confetti(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        if self.r() < 0.3:
            b = self.get(x, y+1)
            if b == EMPTY: self.move_cell(x, y, x, y+1); return
        # Horizontal flutter for festive movement
        if self.r() < 0.5:
            d = -1 if self.r() < 0.5 else 1
            if self.is_empty(x+d, y): self.move_cell(x, y, x+d, y); return
            if self.is_empty(x-d, y): self.move_cell(x, y, x-d, y); return
        # Occasional upward flutter
        if self.r() < 0.08 and self.is_empty(x, y-1):
            self.move_cell(x, y, x, y-1)

    def update_metal(self, x, y):
        i = self.idx(x, y)
        heat = 0
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                if self.get(x+dx, y+dy) == MOLTEN_METAL:
                    heat += 1
        if heat > 0:
            v = min(int(self.life[i]) + heat, 65535)
            self.life[i] = v
            if v >= 200:
                self.set_cell(x, y, MOLTEN_METAL)

    def update_rust(self, x, y):
        i = self.idx(x, y)
        near_water = False
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                if self.get(x+dx, y+dy) == WATER: near_water = True
        self.dec_life(i, 2 if near_water else 1)
        if self.life[i] <= 0: self.set_cell(x, y, ASH)

    def update_concrete(self, x, y):
        pass

    def update_rubber(self, x, y):
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES) and self.r() < 0.08:
            self.set_cell(x, y, OIL); return

    def update_cotton(self, x, y):
        for dx2, dy2 in self._NBR8:
            n = self.get(x+dx2, y+dy2)
            if n in self._HEAT_SOURCES and self.r() < 0.15:
                self.set_cell(x, y, FIRE); self.life[self.idx(x,y)] = self.ri(30, 60)
                if self.is_empty(x, y-1): self.set_cell(x, y-1, SMOKE)
                return
            if n == WATER and self.r() < 0.005: self.set_cell(x, y, MUD); return

    def update_wax(self, x, y):
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES) and self.r() < 0.06:
            self.set_cell(x, y, OIL); return

    def update_fuse(self, x, y):
        i = self.idx(x, y)
        if self.life[i] > 0:
            self.dec_life(i)
            if self.life[i] <= 0: self.explode(x, y, 5); return
        elif self._any_neighbor_in(x, y, self._HEAT_SOURCES):
            self.life[i] = self.ri(150, 250)

    def update_cobweb(self, x, y):
        for dx2, dy2 in self._NBR8:
            if self.get(x+dx2, y+dy2) in self._POWDERS:
                self.moved[self.idx(x+dx2, y+dy2)] = self.frame
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES) and self.r() < 0.1:
            self.set_cell(x, y, SMOKE); return

    def update_copper(self, x, y):
        for dx2, dy2 in self._NBR8:
            nx, ny, n = x+dx2, y+dy2, self.get(x+dx2, y+dy2)
            if n == WATER and self.r() < 0.002: self.set_cell(x, y, RUST); return
            if n == ACID and self.r() < 0.005:
                self.set_cell(nx, ny, TOXIC_GAS); self.clear_cell(x, y); return
            if n in (LAVA, MOLTEN_METAL, PLASMA) and self.r() < 0.01:
                self.set_cell(x, y, MOLTEN_METAL); self.life[self.idx(x,y)] = self.ri(200, 400); return
            if n == FIRE and self.r() < 0.003:
                self.set_cell(x, y, MOLTEN_METAL); self.life[self.idx(x,y)] = self.ri(200, 400); return

    def update_dynamite(self, x, y):
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES): self.explode(x, y, 8); return
        self.fall_pow(x, y)

    def update_molten_metal(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.set_cell(x, y, METAL); return
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                nx, ny, n = x+dx, y+dy, self.get(x+dx, y+dy)
                # Molten-metal-specific: water/ice quenches to solid metal + steam
                if self._check_quench(x, y, nx, ny, n, MOLTEN_METAL): return
                # Molten-metal-specific: sand → glass
                if n == SAND and self.r() < 0.005: self.set_cell(nx, ny, GLASS); return
                # Molten-metal-specific: THERMITE → ember
                if n == THERMITE and self.r() < 0.03:
                    self.set_cell(nx, ny, EMBER); self.life[self.idx(nx, ny)] = 120; return
                # Use shared heat reaction table
                if self._react_heat(nx, ny, n, prob_mult=0.5, allow_explode_prob=True):
                    return
        self.liquid_move(x, y, fall_prob=0.3, spread_prob=0.15, sink_all_liq=True, spread_independent=True)

    def update_spark(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                nx, ny, n = x+dx, y+dy, self.get(x+dx, y+dy)
                # Spark-specific: salt → glass
                if n == SALT and self.r() < 0.01: self.set_cell(nx, ny, GLASS); return
                # Use shared heat reaction table
                if self._react_heat(nx, ny, n, prob_mult=2.0, allow_explode_prob=True):
                    return
        if self.r() < 0.7:
            dx, dy = self._shuffled_dirs()[0]
            if self.is_empty(x+dx, y+dy): self.move_cell(x, y, x+dx, y+dy)

    def update_methane(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                if self.get(x+dx, y+dy) in (FIRE, LAVA, EMBER, SPARK, PLASMA):
                    self.explode(x, y, 7); return
        self.gas_move(x, y, rise_prob=0.7, side_prob=0.4)

    # ---- New elements (IDs 51-65) ----

    def update_blood(self, x, y):
        # Fire burns blood → smoke (handled by IGNITE_ON_HEAT)
        # Water dilutes blood
        if self.r() < 0.003:
            for dx2, dy2 in self._NBR8:
                if self.get(x+dx2, y+dy2) == WATER:
                    self.clear_cell(x, y); return
        # Blood is viscous — slow fall
        self.liquid_move(x, y, fall_prob=0.25, spread_prob=0.06, diag_prob=0.15)

    def update_lichen(self, x, y):
        if self.r() < 0.004:
            _grow_on = (STONE, METAL, BRICK, CONCRETE, MOSAIC, BONE)
            for dx, dy in self._shuffled_dirs():
                nx, ny = x+dx, y+dy
                if self.get(nx, ny) in _grow_on and self.r() < 0.3:
                    self.set_cell(nx, ny, LICHEN); return

    def update_fungus(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0:
            self.set_cell(x, y, DUST); return
        # Spread: fungus grows onto adjacent organic or porous materials
        if self.r() < 0.008:
            _grow_on = (WOOD, PLANT, COTTON, SEED, LICHEN)
            _moisture = (WATER, STEAM, MUD, SLIME, HONEY)
            for dx, dy in self._shuffled_dirs():
                nx, ny = x+dx, y+dy
                n = self.get(nx, ny)
                if n in _grow_on and self.r() < 0.25:
                    self.set_cell(nx, ny, FUNGUS); return
                if n == EMPTY:
                    # Check if near moisture
                    for ddx, ddy in self._NBR8:
                        if self.get(nx+ddx, ny+ddy) in _moisture:
                            if self.r() < 0.08:
                                self.set_cell(nx, ny, FUNGUS); return
                            break

    def update_magnesium(self, x, y):
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                nx, ny, n = x+dx, y+dy, self.get(x+dx, y+dy)
                # Water reacts with magnesium → hydrogen + fire
                if n == WATER and self.r() < 0.015:
                    self.set_cell(x, y, FIRE); self.life[self.idx(x, y)] = self.ri(120, 200)
                    self.set_cell(nx, ny, HYDROGEN); return
                # Fire/ember ignites magnesium → bright plasma fire
                if n in (FIRE, EMBER, SPARK, LAVA, PLASMA) and self.r() < 0.08:
                    self.set_cell(x, y, FIRE); self.life[self.idx(x, y)] = self.ri(150, 220); return
                # Acid → hydrogen gas
                if n == ACID and self.r() < 0.03:
                    self.set_cell(x, y, HYDROGEN); self.set_cell(nx, ny, SALT); return
        self.fall_pow(x, y)

    def update_charcoal(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.set_cell(x, y, ASH); return
        # Charcoal burns very slowly, long-lasting (handled by IGNITE_ON_HEAT with low prob)
        # Charcoal absorbs toxic gas — purifies nearby air
        for dx2, dy2 in self._NBR8:
            n = self.get(x+dx2, y+dy2)
            if n == TOXIC_GAS and self.r() < 0.02:
                self.clear_cell(x+dx2, y+dy2); return
            if n == POISON and self.r() < 0.01:
                self.clear_cell(x+dx2, y+dy2); return
        self.fall_pow(x, y)

    def update_resin(self, x, y):
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES) and self.r() < 0.05:
            self.set_cell(x, y, OIL); return
        # Resin very slowly fossilizes into amber
        if self.r() < 0.0002:
            self.set_cell(x, y, AMBER); return
        self._catch_powders(x, y, 0.03)

    def update_brick(self, x, y):
        if self._any_neighbor_in(x, y, (PLASMA,)) and self.r() < 0.002:
            self.set_cell(x, y, LAVA); return
        if self.r() < 0.001:
            hit = self._find_neighbor(x, y, (WATER,))
            if hit and self.r() < 0.3: self.set_cell(hit[0], hit[1], MUD)

    def update_mosaic(self, x, y):
        if self._any_neighbor_in(x, y, (PLASMA,)) and self.r() < 0.005:
            self.clear_cell(x, y)

    def update_bone(self, x, y):
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES) and self.r() < 0.005:
            self.set_cell(x, y, CHARCOAL); return
        hit = self._find_neighbor(x, y, (MERCURY,))
        if hit and self.r() < 0.003: self.set_cell(x, y, POISON)

    def update_bubble(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        # Bubbles pop on contact with fire or sharp solids
        for dx2, dy2 in self._NBR8:
            n = self.get(x+dx2, y+dy2)
            if n in self._HEAT_SOURCES:
                self.clear_cell(x, y); return
            if n in (STONE, GLASS, METAL, BRICK, CONCRETE, MOSAIC, BONE) and self.r() < 0.15:
                self.clear_cell(x, y); return
        # Bubbles rise quickly in liquids, normal rise otherwise
        has_liquid = False
        for dx2, dy2 in ((0,-1),(0,1),(-1,0),(1,0)):
            if self.is_liq(self.get(x+dx2, y+dy2)):
                has_liquid = True; break
        if has_liquid:
            self.gas_move(x, y, rise_prob=0.9, side_prob=0.2)
        else:
            self.gas_move(x, y, rise_prob=0.6, side_prob=0.35)

    def update_ozone(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        for dx2, dy2 in self._NBR8:
            nx, ny, n = x+dx2, y+dy2, self.get(x+dx2, y+dy2)
            # Ozone neutralizes toxic gas and poison
            if n == TOXIC_GAS and self.r() < 0.04:
                self.clear_cell(nx, ny); self.clear_cell(x, y); return
            if n == POISON and self.r() < 0.02:
                self.clear_cell(nx, ny); self.set_cell(x, y, SMOKE)
                self.life[self.idx(x, y)] = self.ri(10, 20); return
            # Ozone accelerates combustion — acts as strong oxidizer
            if n == FIRE and self.r() < 0.15:
                self.life[self.idx(nx, ny)] = min(int(self.life[self.idx(nx, ny)]) + 15, 65535)
            # Ozone + fungus → fungus dies (ozone is antifungal)
            if n == FUNGUS and self.r() < 0.03:
                self.set_cell(nx, ny, ASH); return
            # Heat source → chain explode
            if n in (FIRE, LAVA, EMBER, SPARK, PLASMA) and self.r() < 0.06:
                self.explode(x, y, 4); return
        self.gas_move(x, y, rise_prob=0.5, side_prob=0.35)

    def update_plasma(self, x, y):
        i = self.idx(x, y); self.dec_life(i, 2)  # Burns out faster
        if self.life[i] <= 0:
            if self.r() < 0.3: self.set_cell(x, y, EMBER)
            elif self.r() < 0.5: self.set_cell(x, y, SMOKE)
            else: self.clear_cell(x, y)
            return
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                nx, ny, n = x+dx, y+dy, self.get(x+dx, y+dy)
                # Plasma is extremely hot — almost everything melts/burns
                if self._check_quench(x, y, nx, ny, n, PLASMA): return
                if n == ICE:
                    self.set_cell(nx, ny, STEAM); return
                if n == STONE and self.r() < 0.008:
                    self.set_cell(nx, ny, LAVA); return
                if n == METAL and self.r() < 0.015:
                    self.set_cell(nx, ny, MOLTEN_METAL); self.life[self.idx(nx, ny)] = self.ri(300, 500); return
                if n == BRICK and self.r() < 0.004:
                    self.set_cell(nx, ny, LAVA); return
                if n == CONCRETE and self.r() < 0.003:
                    self.clear_cell(nx, ny); return
                if n == GLASS and self.r() < 0.02:
                    self.clear_cell(nx, ny); return
                if n == SAND and self.r() < 0.02:
                    self.set_cell(nx, ny, GLASS); return
                if n == BONE and self.r() < 0.03:
                    self.set_cell(nx, ny, ASH); return
                # Plasma ignites things very aggressively — use heat table with high multiplier
                if self._react_heat(nx, ny, n, prob_mult=3.0, allow_explode_prob=True):
                    return
        # Plasma moves: mostly rises, but also darts sideways unpredictably
        if self.r() < 0.7:
            if self.is_empty(x, y-1): self.move_cell(x, y, x, y-1); return
            above = self.get(x, y-1)
            if self.is_gas(above) and above != PLASMA:
                self.swap_cells(x, y, x, y-1); return
        if self.r() < 0.5:
            d = -1 if self.r() < 0.5 else 1
            if self.is_empty(x+d, y-1): self.move_cell(x, y, x+d, y-1); return
            if self.is_empty(x-d, y-1): self.move_cell(x, y, x-d, y-1); return
        if self.r() < 0.6:
            d = -1 if self.r() < 0.5 else 1
            if self.is_empty(x+d, y): self.move_cell(x, y, x+d, y); return
            if self.is_empty(x-d, y): self.move_cell(x, y, x-d, y)

    def update_cotton_candy(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        # Cotton candy dissolves instantly in water
        for dx2, dy2 in self._NBR8:
            if self.get(x+dx2, y+dy2) == WATER:
                self.clear_cell(x, y); return
        # Falls slowly, flutters like confetti but more floaty
        if self.r() < 0.2:
            b = self.get(x, y+1)
            if b == EMPTY: self.move_cell(x, y, x, y+1); return
        if self.r() < 0.6:
            d = -1 if self.r() < 0.5 else 1
            if self.is_empty(x+d, y): self.move_cell(x, y, x+d, y); return
            if self.is_empty(x-d, y): self.move_cell(x, y, x-d, y); return
        if self.r() < 0.15 and self.is_empty(x, y-1):
            self.move_cell(x, y, x, y-1)

    def update_dark_matter(self, x, y):
        i = self.idx(x, y); self.dec_life(i, 3)
        if self.life[i] <= 0:
            # Dark matter decays → leaves void briefly, then nothing
            if self.r() < 0.1: self.set_cell(x, y, VOID_E)
            else: self.clear_cell(x, y)
            return
        # Dark matter devours adjacent particles
        for dx2, dy2 in self._NBR8:
            nx, ny = x+dx2, y+dy2
            n = self.get(nx, ny)
            if n > 0 and n != DARK_MATTER and n != VOID_E and n != STONE and n != CONCRETE and n != BRICK and n != PLASMA:
                if self.r() < 0.025:
                    self.clear_cell(nx, ny)
                    # Feeding extends life
                    v = min(int(self.life[i]) + 50, 65535)
                    self.life[i] = v
                    return
        # Dark matter is stationary but occasionally shifts slightly
        if self.r() < 0.02:
            d = -1 if self.r() < 0.5 else 1
            if self.is_empty(x+d, y): self.move_cell(x, y, x+d, y)

    def update_honey(self, x, y):
        self._catch_powders(x, y, 0.02)
        self.liquid_move(x, y, fall_prob=0.2, spread_prob=0.04, diag_prob=0.1)

    def update_tar(self, x, y):
        self._catch_powders(x, y, 0.03)
        self.liquid_move(x, y, fall_prob=0.15, spread_prob=0.03, diag_prob=0.08)

    def update_ink(self, x, y):
        # Ink flows like water but stains solids it touches
        if self.r() < 0.006:
            for dx2, dy2 in self._NBR8:
                n = self.get(x+dx2, y+dy2)
                # Ink stains porous solids permanently
                if n in (WOOD, COTTON, LICHEN) and self.r() < 0.4:
                    self.color_var[self.idx(x+dx2, y+dy2)] = self.ri(0, 10)
        self.liquid_move(x, y, fall_prob=0.6, spread_prob=0.2)

    def update_vine(self, x, y):
        # Heat destroys vine (handled by IGNITE_ON_HEAT)
        # Vine grows upward aggressively, faster than plant
        if self.r() < 0.012:
            waters = []
            for dx2, dy2 in self._NBR8:
                n = self.get(x+dx2, y+dy2)
                if n == WATER: waters.append((x+dx2, y+dy2))
            if waters:
                wx, wy = waters[self.ri(0, len(waters) - 1)]
                # Grow upward preferentially
                grow_dirs = [(0,-1),(-1,-1),(1,-1),(-1,0),(1,0)]
                d = grow_dirs[self.ri(0, len(grow_dirs) - 1)]
                nx, ny = x+d[0], y+d[1]
                n = self.get(nx, ny)
                if n == EMPTY:
                    self.set_cell(nx, ny, VINE); self.clear_cell(wx, wy)
                elif n in (WOOD, STONE, BRICK, CONCRETE, MOSAIC):
                    # Vine can climb walls
                    if self.is_empty(x, y-1):
                        self.set_cell(x, y-1, VINE); self.clear_cell(wx, wy)

    def update_dry_ice(self, x, y):
        # Dry ice sublimates into CO2 gas, has strong cold aura
        for dx2, dy2 in self._NBR8:
            nx, ny = x+dx2, y+dy2
            n = self.get(nx, ny)
            if self._react_cold(nx, ny, n, prob_mult=1.5): return
            if n == TOXIC_GAS and self.r() < 0.01:
                self.clear_cell(nx, ny); return
            if n in self._HEAT_SOURCES and self.r() < 0.05:
                self.set_cell(nx, ny, STEAM)
        # Sublimate slowly
        if self.r() < 0.003:
            d = -1 if self.r() < 0.5 else 1
            nx, ny = (x, y-1) if self.is_empty(x, y-1) else (x+d, y-1) if self.is_empty(x+d, y-1) else (None, None)
            if nx is not None:
                self.set_cell(nx, ny, CO2); self.clear_cell(x, y)

    def update_co2(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        # CO2 suffocates fire
        for dx2, dy2 in self._NBR8:
            n = self.get(x+dx2, y+dy2)
            if n == FIRE and self.r() < 0.08:
                self.set_cell(x+dx2, y+dy2, SMOKE); return
            # CO2 feeds plants/vines — consumed for growth
            if n in (PLANT, VINE) and self.r() < 0.003:
                self.clear_cell(x, y); return
        # CO2 is heavy — sinks
        if self.r() < 0.3 and self.is_empty(x, y+1):
            self.move_cell(x, y, x, y+1); return
        self.gas_move(x, y, rise_prob=0.15, side_prob=0.25)

    def update_phosphorus(self, x, y):
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                nx, ny, n = x+dx, y+dy, self.get(x+dx, y+dy)
                # Phosphorus ignites in water (exothermic reaction)
                if n == WATER and self.r() < 0.01:
                    self.set_cell(x, y, FIRE); self.life[self.idx(x, y)] = self.ri(60, 100)
                    self.set_cell(nx, ny, STEAM); return
                # Spontaneously ignites near any heat
                if n in self._HEAT_SOURCES and self.r() < 0.15:
                    self.set_cell(x, y, FIRE); self.life[self.idx(x, y)] = self.ri(80, 130); return
                # Acid reacts violently
                if n == ACID and self.r() < 0.03:
                    self.set_cell(x, y, FIRE); self.clear_cell(nx, ny); return
        # Slow spontaneous ignition in air
        if self.r() < 0.0003:
            self.set_cell(x, y, FIRE); self.life[self.idx(x, y)] = self.ri(40, 70); return
        self.fall_pow(x, y)

    def update_grain(self, x, y):
        for dx2, dy2 in self._NBR8:
            n = self.get(x+dx2, y+dy2)
            if n in (WATER, MUD) and self.r() < 0.015:
                self.set_cell(x, y, PLANT); self.clear_cell(x+dx2, y+dy2); return
            if n in self._HEAT_SOURCES and self.r() < 0.02:
                self.set_cell(x, y, FIRE); self.life[self.idx(x, y)] = self.ri(15, 30); return
        self.fall_pow(x, y)

    def update_fat(self, x, y):
        # Fat dissolves slowly in water
        if self.r() < 0.002:
            hit = self._find_neighbor(x, y, (WATER,))
            if hit: self.clear_cell(x, y); return
        self._catch_powders(x, y, 0.04)

    def update_amber(self, x, y):
        # Amber is fossilized resin — very inert, only melts under extreme heat
        # Already handled by IGNITE_ON_HEAT → OIL
        pass

    def update_radioactive(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.set_cell(x, y, GLASS); return
        # Emit sparks randomly
        if self.r() < 0.008:
            dx, dy = self._shuffled_dirs()[0]
            if self.is_empty(x+dx, y+dy): self.set_cell(x+dx, y+dy, SPARK)
        # Poison nearby organic matter
        if self.r() < 0.015:
            hit = self._find_neighbor(x, y, self._ORGANICS)
            if hit and self.r() < 0.3: self.set_cell(hit[0], hit[1], TOXIC_GAS)
        # Radiation heats nearby water into steam slowly
        if self.r() < 0.005:
            hit = self._find_neighbor(x, y, (WATER,))
            if hit: self.set_cell(hit[0], hit[1], STEAM)

    def update_feather(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0: self.clear_cell(x, y); return
        # Dissolves in water
        if self._any_neighbor_in(x, y, (WATER,)):
            self.clear_cell(x, y); return
        # Feather falls extremely slowly, drifts sideways dramatically
        if self.r() < 0.1:
            b = self.get(x, y+1)
            if b == EMPTY: self.move_cell(x, y, x, y+1); return
        # Strong horizontal drift
        if self.r() < 0.75:
            d = -1 if self.r() < 0.5 else 1
            if self.is_empty(x+d, y): self.move_cell(x, y, x+d, y); return
            if self.is_empty(x-d, y): self.move_cell(x, y, x-d, y); return
        # Occasional updraft
        if self.r() < 0.25 and self.is_empty(x, y-1):
            self.move_cell(x, y, x, y-1)

    def update_glacier(self, x, y):
        if self._any_neighbor_in(x, y, (PLASMA,)) and self.r() < 0.001:
            self.set_cell(x, y, WATER); return
        hit = self._find_neighbor(x, y, (LAVA,))
        if hit and self.r() < 0.002:
            self.set_cell(x, y, WATER); self.set_cell(hit[0], hit[1], STONE); return
        # Strong cold aura (stronger than ice)
        if self.r() < 0.01:
            for dx2, dy2 in self._NBR8:
                if self._react_cold(x+dx2, y+dy2, self.get(x+dx2, y+dy2), prob_mult=1.2):
                    return

    def update_electrical(self, x, y):
        i = self.idx(x, y); self.dec_life(i)
        if self.life[i] <= 0:
            if self.r() < 0.2: self.set_cell(x, y, SMOKE)
            else: self.clear_cell(x, y)
            return
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dx==0 and dy==0: continue
                nx, ny, n = x+dx, y+dy, self.get(x+dx, y+dy)
                # Water + electrical = more electrical (conducts)
                if n == WATER and self.r() < 0.04:
                    self.set_cell(nx, ny, ELECTRICAL)
                    self.life[self.idx(nx, ny)] = self.ri(10, 25); return
                # Metal conducts — sparks travel through metal
                if n == METAL and self.r() < 0.02:
                    for ddx, ddy in self._NBR8:
                        nn = self.get(nx+ddx, ny+ddy)
                        if nn == EMPTY and self.r() < 0.3:
                            self.set_cell(nx+ddx, ny+ddy, ELECTRICAL)
                            self.life[self.idx(nx+ddx, ny+ddy)] = self.ri(8, 18); return
                # Radioactive + electrical = massive chain reaction
                if n == RADIOACTIVE and self.r() < 0.05:
                    self.explode(nx, ny, 6); return
                # Ignites flammables
                if n in (OIL, NAPALM, GAS, HYDROGEN, METHANE) and self.r() < 0.12:
                    self.set_cell(nx, ny, FIRE); return
                # Gunpowder/dynamite/nitro explode
                if n in (GUNPOWDER, DYNAMITE, NITRO):
                    self.explode(nx, ny, self.EXPLODE_ON_HEAT.get(n, 5)); return
        # Electrical arcs move erratically
        if self.r() < 0.6:
            dx, dy = self._shuffled_dirs()[0]
            nx, ny = x+dx, y+dy
            if self.is_empty(nx, ny):
                self.move_cell(x, y, nx, ny)
            elif self.is_gas(self.get(nx, ny)):
                self.swap_cells(x, y, nx, ny)

    def update_mudstone(self, x, y):
        hit = self._find_neighbor(x, y, (WATER,))
        if hit and self.r() < 0.008: self.set_cell(x, y, MUD); return
        if self._any_neighbor_in(x, y, self._HEAT_SOURCES) and self.r() < 0.003:
            self.set_cell(x, y, SAND)

    def update_antimatter(self, x, y):
        i = self.idx(x, y); self.dec_life(i, 2)
        if self.life[i] <= 0:
            if self.r() < 0.15: self.set_cell(x, y, VOID_E)
            else: self.clear_cell(x, y)
            return
        # Antimatter annihilates ANY adjacent particle — both destroyed, creates spark
        for dx2, dy2 in self._NBR8:
            nx, ny = x+dx2, y+dy2
            n = self.get(nx, ny)
            if n > 0 and n != ANTIMATTER:
                if self.r() < 0.04:
                    self.clear_cell(nx, ny)
                    # Annihilation produces energy
                    if self.r() < 0.4:
                        self.set_cell(x, y, FIRE); self.life[self.idx(x, y)] = self.ri(30, 60)
                    elif self.r() < 0.5:
                        self.set_cell(x, y, SPARK)
                    else:
                        self.clear_cell(x, y)
                    return
        # Drifts slowly
        if self.r() < 0.03:
            d = -1 if self.r() < 0.5 else 1
            if self.is_empty(x+d, y): self.move_cell(x, y, x+d, y)

    UPDATE_MAP = {
        SAND: update_sand, WATER: update_water, FIRE: update_fire, SMOKE: update_smoke, LAVA: update_lava,
        OIL: update_oil, ACID: update_acid, WOOD: update_wood, GUNPOWDER: update_gunpowder,
        STEAM: update_steam, ICE: update_ice, PLANT: update_plant, GAS: update_gas,
        VOID_E: update_void, SALT: update_salt, DUST: update_dust, MUD: update_mud,
        GLASS: update_glass, CLONE: update_clone, EMBER: update_ember, THERMITE: update_thermite,
        SNOW: update_snow, ASH: update_ash, COAL: update_coal, GRAVEL: update_gravel,
        SEED: update_seed, SULFUR: update_sulfur, MERCURY: update_mercury, NAPALM: update_napalm,
        SLIME: update_slime, POISON: update_poison, NITRO: update_nitro, HYDROGEN: update_hydrogen,
        TOXIC_GAS: update_toxic_gas, NITROUS: update_nitrous, CONFETTI: update_confetti,
        METAL: update_metal, RUST: update_rust, CONCRETE: update_concrete, RUBBER: update_rubber,
        COTTON: update_cotton, WAX: update_wax, FUSE: update_fuse, COBWEB: update_cobweb,
        COPPER: update_copper, DYNAMITE: update_dynamite, MOLTEN_METAL: update_molten_metal,
        SPARK: update_spark, METHANE: update_methane,
        BLOOD: update_blood, LICHEN: update_lichen, FUNGUS: update_fungus,
        MAGNESIUM: update_magnesium, CHARCOAL: update_charcoal, RESIN: update_resin,
        BRICK: update_brick, MOSAIC: update_mosaic, BONE: update_bone,
        BUBBLE: update_bubble, OZONE: update_ozone, PLASMA: update_plasma,
        COTTON_CANDY: update_cotton_candy, DARK_MATTER: update_dark_matter, HONEY: update_honey,
        TAR: update_tar, INK: update_ink, VINE: update_vine, DRY_ICE: update_dry_ice,
        CO2: update_co2, PHOSPHORUS: update_phosphorus, GRAIN: update_grain,
        FAT: update_fat, AMBER: update_amber, RADIOACTIVE: update_radioactive,
        FEATHER: update_feather, GLACIER: update_glacier, ELECTRICAL: update_electrical,
        MUDSTONE: update_mudstone, ANTIMATTER: update_antimatter,
    }
    # Fast lookup array: UPDATE_FN[type] = function or None
    _UPDATE_FN = [None] * 81
    for _tid, _fn in UPDATE_MAP.items():
        _UPDATE_FN[_tid] = _fn

    def update_sim(self):
        self.frame += 1
        frame = self.frame
        grid = self.grid
        moved = self.moved
        ufn = self._UPDATE_FN
        W, H = self.W, self.H
        ltr = frame % 2 == 0
        sx, ex, dx = (0, W, 1) if ltr else (W - 1, -1, -1)
        for y in range(H - 1, -1, -1):
            yw = y * W
            for x in range(sx, ex, dx):
                i = yw + x
                if moved[i] == frame: continue
                fn = ufn[grid[i]]
                if fn: fn(self, x, y)

    # --- Brush (pure sim logic, called from widget input handlers) ---

    def brush_at(self, gx, gy, erasing=False, density=0.65):
        t = EMPTY if erasing else self.selected_type
        r = self.brush_size
        for dy in range(-r, r+1):
            for dx in range(-r, r+1):
                if dx*dx + dy*dy > r*r: continue
                nx, ny = gx+dx, gy+dy
                if not self.in_b(nx, ny): continue
                if t == EMPTY: self.clear_cell(nx, ny)
                elif self.get(nx, ny) == EMPTY and self.r() < density:
                    self.set_cell(nx, ny, t)

    def brush_at_adaptive(self, gx, gy, erasing=False):
        """Speed-adaptive brush: slower movement = denser fill."""
        now = time.time()
        dx = gx - self._last_brush_gx
        dy = gy - self._last_brush_gy
        dt = now - self._last_brush_time
        dist = (dx*dx + dy*dy) ** 0.5

        # Base density 0.65, ramp up to 0.95 for slow/sationary, down to 0.3 for fast
        if dt > 0.001:
            speed = dist / dt  # grid cells per second
        else:
            speed = 0.0

        # Map speed to density: speed 0 -> 0.95, speed 500+ -> 0.30
        density = max(0.30, min(0.95, 0.95 - speed * 0.0013))

        self.brush_at(gx, gy, erasing, density)
        self._last_brush_time = now
        self._last_brush_gx = gx
        self._last_brush_gy = gy

    def bresenham(self, x0, y0, x1, y1, erasing=False):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = -1 if x0 > x1 else 1; sy = -1 if y0 > y1 else 1; err = dx - dy
        while True:
            self.brush_at(x0, y0, erasing)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x0 += sx
            if e2 < dx: err += dx; y0 += sy

    def bresenham_adaptive(self, x0, y0, x1, y1, erasing=False):
        """Bresenham with speed-adaptive density."""
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = -1 if x0 > x1 else 1; sy = -1 if y0 > y1 else 1; err = dx - dy
        while True:
            self.brush_at_adaptive(x0, y0, erasing)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x0 += sx
            if e2 < dx: err += dx; y0 += sy

    def flood_fill(self, gx, gy, fill_type):
        """Flood fill from (gx, gy) replacing connected cells of the same type."""
        if not self.in_b(gx, gy): return
        target = self.grid[self.idx(gx, gy)]
        if target == fill_type: return

        visited = set()
        queue = deque([(gx, gy)])
        visited.add((gx, gy))
        max_fill = 50000  # safety limit
        filled = 0

        while queue and filled < max_fill:
            cx, cy = queue.popleft()
            self.set_cell(cx, cy, fill_type)
            filled += 1

            for ddx, ddy in self._NBR8:
                nx, ny = cx + ddx, cy + ddy
                if (nx, ny) in visited: continue
                if not self.in_b(nx, ny): continue
                if self.grid[self.idx(nx, ny)] != target: continue
                visited.add((nx, ny))
                queue.append((nx, ny))

    # --- Undo system ---

    def save_snapshot(self):
        """Save current grid state for undo (call at stroke start)."""
        self._stroke_snapshot = (
            self.grid.copy(),
            self.color_var.copy(),
            self.life.copy(),
        )

    def push_undo(self):
        """Push the stroke snapshot to undo stack (call at stroke end)."""
        if self._stroke_snapshot is None: return
        self._undo_stack.append(self._stroke_snapshot)
        if len(self._undo_stack) > self._undo_limit:
            self._undo_stack.pop(0)
        self._stroke_snapshot = None

    def undo(self):
        """Restore the most recent undo snapshot."""
        if not self._undo_stack: return False
        grid, color_var, life = self._undo_stack.pop()
        self.grid[:] = grid
        self.color_var[:] = color_var
        self.life[:] = life
        return True


# ================================================================
# GL RENDERER — encapsulates all OpenGL state, shaders, FBOs
# ================================================================
class SandRenderer:
    """Manages the GPU rendering pipeline for the falling-sand sim.

    Pipeline (3 draw calls + hardware mipmap generation):
        1. Scene pass:      data texture -> full-res FBO  (elemColor + edge darkening)
        2. Bloom extract:   scene FBO   -> half-res FBO   (brightness threshold + 2x2 downsample)
        3. Mipmap gen:      hardware-accelerated multi-scale blur on bloom texture
        4. Composite pass:  scene + bloom mips -> screen  (additive blend + vignette)

    Replaces the old 10-pass pipeline (8 Gaussian blur draws) with a mipmap-based
    approach that produces equivalent visual quality at ~60% less GPU cost.
    """

    def __init__(self, sim_w, sim_h):
        self.sim_w = sim_w
        self.sim_h = sim_h
        self._initialized = False
        self._needs_reinit = False  # Set to True when context loss is detected

    # ---- public API ----

    def initialize(self):
        """Call inside a valid GL context (e.g. initializeGL)."""
        ver = glGetString(GL_VERSION).decode()
        ren = glGetString(GL_RENDERER).decode()
        print(f"OpenGL {ver} -- {ren}")

        glClearColor(0.047, 0.039, 0.031, 1.0)

        # -- shared vertex shader + fullscreen quad VAO --
        self._vs = self._compile_shader(GL_VERTEX_SHADER, VERT_SRC)
        self._vao = glGenVertexArrays(1)
        self._vbo = glGenBuffers(1)
        glBindVertexArray(self._vao)
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)
        glBufferData(GL_ARRAY_BUFFER,
                     np.array([-1, -1, 1, -1, -1, 1, 1, 1], dtype=np.float32),
                     GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        glBindVertexArray(0)

        # -- programs & cached uniform locations --
        self._init_programs()

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # -- data texture (R=type, G=var, B=life_lo, A=life_hi) --
        self._data_tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._data_tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.sim_w, self.sim_h, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, None)

        # -- FBOs --
        self._fbo_scene, self._tex_scene = self._make_fbo(self.sim_w, self.sim_h)
        # Scene texture: NEAREST for pixel-art sharpness
        glBindTexture(GL_TEXTURE_2D, self._tex_scene)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # Bloom FBO at half-res with full mip chain for mipmap-based bloom
        bw, bh = self.sim_w // 2, self.sim_h // 2
        self._bloom_size = (bw, bh)
        self._fbo_bloom, self._tex_bloom = self._make_bloom_fbo(bw, bh)

        # -- pre-allocated CPU staging buffer (reused every frame) --
        self._packed = np.empty((self.sim_w * self.sim_h, 4), dtype=np.uint8)

        self._initialized = True
        self._needs_reinit = False

    def render(self, grid, color_var, life, frame, bloom_intensity, screen_w, screen_h):
        """Upload sim state and draw one frame.

        Parameters
        ----------
        grid, color_var : np.ndarray (W*H, uint8)
        life            : np.ndarray (W*H, uint16)
        frame           : int   -- current simulation frame (used as u_time)
        bloom_intensity : float -- composite bloom strength
        screen_w, screen_h : int -- widget pixel size for glViewport
        """
        # -- CRITICAL: Drain stale GL errors from Qt's internal FBO management --
        # OpenGL_accelerate reports errors lazily.  Qt's internal compositing can
        # leave a stale GL error in the queue that surfaces on OUR first GL call.
        # Draining here prevents false GLError on glActiveTexture().
        while glGetError() != GL_NO_ERROR:
            pass

        # -- Reset GL state (QOpenGLWidget leaves state dirty between frames) --
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # -- 1. Upload packed RGBA8 data -> texture --
        self._upload_data(grid, color_var, life)

        # -- 2. Scene pass -> full-res FBO --
        glUseProgram(self._prog_scene)
        glUniform1f(self._loc_scene_time, float(frame))
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self._data_tex)
        glBindFramebuffer(GL_FRAMEBUFFER, self._fbo_scene)
        glViewport(0, 0, self.sim_w, self.sim_h)
        glClear(GL_COLOR_BUFFER_BIT)
        self._draw_quad()

        # -- 3. Bloom extract -> half-res (2x2 downsample + brightness threshold) --
        bw, bh = self._bloom_size
        glUseProgram(self._prog_bloom_extract)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self._tex_scene)
        glBindFramebuffer(GL_FRAMEBUFFER, self._fbo_bloom)
        glViewport(0, 0, bw, bh)
        glClear(GL_COLOR_BUFFER_BIT)
        self._draw_quad()

        # -- 4. Hardware mipmap generation -> free multi-scale blur --
        # Unbind FBO first (some drivers require it before mipmap gen)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindTexture(GL_TEXTURE_2D, self._tex_bloom)
        glGenerateMipmap(GL_TEXTURE_2D)

        # -- 5. Composite -> screen (scene + multi-mip bloom + vignette) --
        glUseProgram(self._prog_composite)
        glUniform1f(self._loc_comp_bloom, bloom_intensity)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self._tex_scene)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self._tex_bloom)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, screen_w, screen_h)
        glClear(GL_COLOR_BUFFER_BIT)
        self._draw_quad()

        # -- Restore clean state for Qt's internal compositing --
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 0)
        glUseProgram(0)

        return True  # Render succeeded

    def resize(self, w, h):
        glViewport(0, 0, w, h)

    def cleanup(self):
        """Delete all GPU resources. Call before GL context is destroyed.
        
        Safe to call multiple times.  Silently ignores errors if resources
        are already invalid (e.g. after an unexpected context loss).
        """
        if not self._initialized:
            return
        try:
            glDeleteVertexArrays(1, [self._vao])
            glDeleteBuffers(1, [self._vbo])
            glDeleteTextures([self._data_tex, self._tex_scene, self._tex_bloom])
            for f in (self._fbo_scene, self._fbo_bloom):
                glDeleteFramebuffers(1, [f])
            for p in (self._prog_scene, self._prog_bloom_extract, self._prog_composite):
                glDetachShader(p, self._vs)
                glDeleteProgram(p)
            glDeleteShader(self._vs)
        except Exception:
            pass  # Resources may already be invalid — that's OK
        finally:
            self._initialized = False
            self._needs_reinit = False

    # ---- internal helpers ----

    def _upload_data(self, grid, color_var, life):
        """Pack sim arrays into RGBA8 and upload directly to texture."""
        pk = self._packed
        pk[:, 0] = grid
        pk[:, 1] = color_var
        pk[:, 2] = life.astype(np.uint8)
        pk[:, 3] = (life >> 8).astype(np.uint8)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self._data_tex)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.sim_w, self.sim_h,
                        GL_RGBA, GL_UNSIGNED_BYTE, pk)

    def _draw_quad(self):
        glBindVertexArray(self._vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    @staticmethod
    def _make_fbo(w, h):
        fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex, 0)
        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if status != GL_FRAMEBUFFER_COMPLETE:
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glDeleteTextures([tex])
            glDeleteFramebuffers(1, [fbo])
            raise RuntimeError(f"FBO incomplete (status=0x{status:04X}, size={w}x{h})")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        return fbo, tex

    @staticmethod
    def _make_bloom_fbo(w, h):
        """Create an FBO with a full mip-chain texture for mipmap-based bloom."""
        fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        # Allocate complete mip chain so glGenerateMipmap can write all levels
        levels = max(w, h).bit_length()
        for level in range(levels):
            lw = max(1, w >> level)
            lh = max(1, h >> level)
            glTexImage2D(GL_TEXTURE_2D, level, GL_RGB, lw, lh, 0,
                         GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex, 0)
        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if status != GL_FRAMEBUFFER_COMPLETE:
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glDeleteTextures([tex])
            glDeleteFramebuffers(1, [fbo])
            raise RuntimeError(f"Bloom FBO incomplete (status=0x{status:04X})")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        return fbo, tex

    def _init_programs(self):
        vs = self._vs
        # Scene program
        self._prog_scene = self._link_program(vs, self._compile_shader(GL_FRAGMENT_SHADER, FRAG_SRC))
        glUseProgram(self._prog_scene)
        glUniform1i(glGetUniformLocation(self._prog_scene, "u_data"), 0)
        self._loc_scene_time = glGetUniformLocation(self._prog_scene, "u_time")
        glUniform2f(glGetUniformLocation(self._prog_scene, "u_res"), self.sim_w, self.sim_h)

        # Bloom extract program
        self._prog_bloom_extract = self._link_program(vs, self._compile_shader(GL_FRAGMENT_SHADER, BLOOM_EXTRACT_SRC))
        glUseProgram(self._prog_bloom_extract)
        glUniform1i(glGetUniformLocation(self._prog_bloom_extract, "u_tex"), 0)

        # Composite program (samples bloom at explicit mip levels via textureLod)
        self._prog_composite = self._link_program(vs, self._compile_shader(GL_FRAGMENT_SHADER, COMPOSITE_SRC))
        glUseProgram(self._prog_composite)
        self._loc_comp_bloom = glGetUniformLocation(self._prog_composite, "u_bloomIntensity")
        glUniform1i(glGetUniformLocation(self._prog_composite, "u_scene"), 0)
        glUniform1i(glGetUniformLocation(self._prog_composite, "u_bloom"), 1)

    @staticmethod
    def _compile_shader(stype, src):
        s = glCreateShader(stype)
        glShaderSource(s, src)
        glCompileShader(s)
        if not glGetShaderiv(s, GL_COMPILE_STATUS):
            log = glGetShaderInfoLog(s).decode()
            glDeleteShader(s)
            raise RuntimeError(f"Shader compile error:\n{log}")
        return s

    @staticmethod
    def _link_program(vs, fs):
        p = glCreateProgram()
        glAttachShader(p, vs)
        glAttachShader(p, fs)
        glLinkProgram(p)
        if not glGetProgramiv(p, GL_LINK_STATUS):
            log = glGetProgramInfoLog(p).decode()
            glDeleteProgram(p)
            glDeleteShader(fs)
            raise RuntimeError(f"Program link error:\n{log}")
        # FS no longer needed once linked -- driver keeps it alive until program destruction.
        glDeleteShader(fs)
        return p


# ================================================================
# OPENGL WIDGET  (Qt shell -- composes SandSimulation + SandRenderer)
#
# Architecture:
#   - Simulation runs on a FIXED-RATE TIMER (decoupled from vsync).
#   - Rendering runs on Qt's paint GL cycle (triggered by update()).
#   - GL context loss is auto-detected and recovered without crashing.
# ================================================================
class SandGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sim = SandSimulation(400, 300)
        self.setMinimumSize(self.sim.W * 2, self.sim.H * 2)
        self.setMouseTracking(True)  # receive mouse move events even without button

        self.bloom_intensity = 0.7
        self.last_time = time.time()
        self.fps = 0.0

        # --- Cursor tracking for brush overlay ---
        self._cursor_x = -1.0  # widget-pixel coords
        self._cursor_y = -1.0
        self._cursor_visible = False

        # --- Shift+click line preview endpoint ---
        self._line_preview_end = None  # (gx, gy) or None

        # Renderer (initialized in initializeGL when GL context is current)
        self._renderer = SandRenderer(self.sim.W, self.sim.H)

        # --- TWO separate timers: sim tick vs. render request ---
        # Simulation runs at a fixed rate regardless of render speed.
        self._sim_timer = QTimer(self)
        self._sim_timer.timeout.connect(self._sim_tick)
        self._sim_timer.start(16)  # ~60 Hz sim tick

        # Render is driven by the default QOpenGLWidget update cycle.
        # We request a repaint after each sim tick.
        self._render_timer = QTimer(self)
        self._render_timer.timeout.connect(self.update)
        self._render_timer.start(16)  # vsync-aligned repaint

    # --- GL lifecycle ---

    def initializeGL(self):
        # Drain any errors left over from context creation
        while glGetError() != GL_NO_ERROR:
            pass

        if self._renderer._initialized:
            self._renderer.cleanup()
        self._renderer.initialize()
        # Ensure GPU resources are freed if the GL context is destroyed at runtime
        try:
            self.context().aboutToBeDestroyed.connect(self._on_context_destroyed)
        except Exception:
            pass

    def _on_context_destroyed(self):
        """Called when Qt is about to destroy the GL context."""
        try:
            self._renderer.cleanup()
        except Exception:
            pass
        self._renderer._needs_reinit = True

    def resizeGL(self, w, h):
        if self._renderer._initialized:
            self._renderer.resize(w, h)

    def _sim_tick(self):
        """Advance the simulation by one step (called by sim timer)."""
        if self.sim.sim_speed > 0:
            for _ in range(self.sim.sim_speed):
                self.sim.update_sim()

    def paintGL(self):
        # --- Auto-recovery: if context was lost, reinitialize ---
        if self._renderer._needs_reinit:
            try:
                # Drain stale errors before reinitializing
                while glGetError() != GL_NO_ERROR:
                    pass
                self._renderer.cleanup()
                self._renderer.initialize()
            except Exception:
                # Context still not ready — skip this frame, try again next time
                return

        if not self._renderer._initialized:
            return

        # --- FPS counter ---
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        if dt > 0:
            self.fps = self.fps * 0.9 + (1.0 / dt) * 0.1
        if self.sim.frame % 10 == 0:
            try:
                cnt = np.count_nonzero(self.sim.grid)
                self.window().stats_label.setText(
                    f"{cnt:,} particles | {self.fps:.0f} FPS"
                )
            except Exception:
                pass  # Window may not exist yet during startup

        # --- Render (with error recovery) ---
        dpr = self.devicePixelRatioF()
        try:
            self._renderer.render(
                grid=self.sim.grid,
                color_var=self.sim.color_var,
                life=self.sim.life,
                frame=self.sim.frame,
                bloom_intensity=self.bloom_intensity,
                screen_w=int(self.width() * dpr),
                screen_h=int(self.height() * dpr),
            )
        except Exception as e:
            # Any GL error during render -> mark for reinit, recover next frame
            print(f"[GL] Render failed ({e}), scheduling reinit...")
            self._renderer._needs_reinit = True

        # --- Brush cursor overlay & line preview (drawn in screen space) ---
        self._draw_cursor_overlay()

    def _draw_cursor_overlay(self):
        """Draw brush circle and shift-line preview overlay using OpenGL lines."""
        if not self._cursor_visible:
            return

        import math as _m

        # Switch to 2D screen-space ortho projection
        w, h = self.width(), self.height()
        dpr = self.devicePixelRatioF()
        glViewport(0, 0, int(w * dpr), int(h * dpr))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, w, h, 0, -1, 1)  # y-down to match widget coords
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        rect = self.contentsRect()
        scale_x = rect.width() / self.sim.W
        scale_y = rect.height() / self.sim.H
        cx_w = rect.x() + self._cursor_x * scale_x
        cy_w = rect.y() + self._cursor_y * scale_y

        r = self.sim.brush_size
        num_seg = max(32, r * 8)
        two_pi = 6.283185307179586

        # --- Brush circle outline ---
        glLineWidth(1.5)
        if self.sim.erasing:
            glColor4f(1.0, 0.35, 0.25, 0.65)  # red tint when erasing
        else:
            glColor4f(1.0, 1.0, 1.0, 0.55)  # white circle
        glBegin(GL_LINE_LOOP)
        for i in range(num_seg):
            a = two_pi * i / num_seg
            glVertex2f(cx_w + r * scale_x * _m.cos(a),
                       cy_w + r * scale_y * _m.sin(a))
        glEnd()

        # --- Crosshair at center ---
        cs = 3
        glColor4f(1.0, 1.0, 1.0, 0.35)
        glBegin(GL_LINES)
        glVertex2f(cx_w - cs, cy_w); glVertex2f(cx_w + cs, cy_w)
        glVertex2f(cx_w, cy_w - cs); glVertex2f(cx_w, cy_w + cs)
        glEnd()

        # --- Shift+click line preview ---
        anchor = self.sim._line_anchor
        if anchor and self._line_preview_end:
            ax = rect.x() + anchor[0] * scale_x
            ay = rect.y() + anchor[1] * scale_y
            ex = rect.x() + self._line_preview_end[0] * scale_x
            ey = rect.y() + self._line_preview_end[1] * scale_y
            # Line from anchor to cursor
            glLineWidth(1.0)
            glColor4f(1.0, 0.42, 0.21, 0.5)
            glBegin(GL_LINES)
            glVertex2f(ax, ay); glVertex2f(ex, ey)
            glEnd()
            # Circle at anchor point
            glBegin(GL_LINE_LOOP)
            for i in range(num_seg):
                a = two_pi * i / num_seg
                glVertex2f(ax + r * scale_x * _m.cos(a),
                           ay + r * scale_y * _m.sin(a))
            glEnd()

        glDisable(GL_BLEND)

    # --- Input (Qt event handlers) ---

    def _c2g(self, cx, cy):
        """Convert widget pixel coords to grid coords."""
        rect = self.contentsRect()
        return (int((cx - rect.x()) * (self.sim.W / rect.width())),
                int((cy - rect.y()) * (self.sim.H / rect.height())))

    def _update_hover_info(self, gx, gy):
        """Update status bar with element info under cursor."""
        try:
            win = self.window()
            if self.sim.in_b(gx, gy):
                t = self.sim.grid[self.sim.idx(gx, gy)]
                name = ELEM_NAME.get(t, "???")
                pos_str = f"({gx}, {gy})"
                key_hint = ELEM_KEY.get(t, "")
                key_str = f" [{key_hint}]" if key_hint else ""
                win.hover_label.setText(f"{name}{key_str} @ {pos_str}")
            else:
                win.hover_label.setText("")
        except Exception:
            pass

    def mousePressEvent(self, event: QMouseEvent):
        modifiers = event.modifiers()
        gx, gy = self._c2g(event.position().x(), event.position().y())

        # Middle-click: eyedropper (pick element)
        if event.button() == Qt.MiddleButton:
            if self.sim.in_b(gx, gy):
                t = self.sim.grid[self.sim.idx(gx, gy)]
                if t != EMPTY:
                    self.sim.selected_type = t
                    self.window()._select_element(t)
                    name = ELEM_NAME.get(t, "???")
                    self.window().hover_label.setText(f"Picked: {name}")
            return

        # Left or Right button
        if event.button() in (Qt.LeftButton, Qt.RightButton):
            self.sim.erasing = (event.button() == Qt.RightButton)

            # Shift+click: set line anchor (straight line mode)
            if modifiers & Qt.ShiftModifier and event.button() == Qt.LeftButton:
                if self.sim._line_anchor is None:
                    self.sim._line_anchor = (gx, gy)
                    self.window().hover_label.setText(f"Line start: ({gx}, {gy}) — click end point")
                    return
                else:
                    # Draw the line from anchor to here
                    self.sim.save_snapshot()
                    self.sim.bresenham(
                        self.sim._line_anchor[0], self.sim._line_anchor[1],
                        gx, gy, self.sim.erasing
                    )
                    self.sim.push_undo()
                    self.sim._line_anchor = None
                    self._line_preview_end = None
                    return

            # Normal draw: save snapshot for undo
            self.sim.save_snapshot()
            self.sim.mouse_down = True
            # Reset adaptive tracking for new stroke
            self.sim._last_brush_time = time.time()
            self.sim._last_brush_gx = gx
            self.sim._last_brush_gy = gy
            self.sim.brush_at(gx, gy, self.sim.erasing)
            self.sim.prev_gx, self.sim.prev_gy = gx, gy

    def mouseMoveEvent(self, event: QMouseEvent):
        cx, cy = event.position().x(), event.position().y()
        gx, gy = self._c2g(cx, cy)

        # Update cursor position for overlay
        self._cursor_x = gx
        self._cursor_y = gy
        self._cursor_visible = True

        # Update hover info
        self._update_hover_info(gx, gy)

        # Update shift+click line preview
        if self.sim._line_anchor is not None:
            self._line_preview_end = (gx, gy)

        # Drawing
        if self.sim.mouse_down:
            if self.sim.prev_gx >= 0:
                self.sim.bresenham_adaptive(
                    self.sim.prev_gx, self.sim.prev_gy, gx, gy, self.sim.erasing
                )
            self.sim.prev_gx, self.sim.prev_gy = gx, gy

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() in (Qt.LeftButton, Qt.RightButton):
            self.sim.push_undo()  # commit stroke to undo stack
            self.sim.mouse_down = False
            self.sim.prev_gx, self.sim.prev_gy = -1, -1

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """Double-click: flood fill at position."""
        if event.button() == Qt.LeftButton:
            gx, gy = self._c2g(event.position().x(), event.position().y())
            self.sim.save_snapshot()
            self.sim.flood_fill(gx, gy, self.sim.selected_type)
            self.sim.push_undo()

    def leaveEvent(self, event):
        """Hide cursor overlay when mouse leaves the widget."""
        self._cursor_visible = False
        self._line_preview_end = None
        try:
            self.window().hover_label.setText("")
        except Exception:
            pass

    def wheelEvent(self, event: QWheelEvent):
        self.sim.brush_size = max(1, min(14, self.sim.brush_size + (1 if event.angleDelta().y() > 0 else -1)))
        self.window().brush_slider.setValue(self.sim.brush_size)


# ================================================================
# MAIN WINDOW
# ================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Falling Sand -- 81 Elements [Mipmap Bloom Pipeline]")
        self.setStyleSheet("""
            QMainWindow { background-color: #12100e; }
            QToolBar { background: #1c1814; border-bottom: 1px solid #2a2218; padding: 6px; spacing: 8px; }
            QComboBox { background: #2a2218; color: #e8ddd0; border: 1px solid #3a3228; border-radius: 6px; padding: 6px 10px; font-size: 14px; min-width: 170px; }
            QComboBox::drop-down { border: none; width: 20px; }
            QComboBox QAbstractItemView { background: #1c1814; color: #e8ddd0; selection-background-color: #ff6b35; }
            QSlider::groove:horizontal { height: 4px; background: #3a3228; border-radius: 2px; }
            QSlider::handle:horizontal { background: #ff6b35; width: 14px; margin: -5px 0; border-radius: 7px; }
            QPushButton { background: #2a2218; color: #e8ddd0; border: 1px solid #3a3228; border-radius: 6px; padding: 6px 12px; }
            QPushButton:hover { background: #3a3228; }
            QPushButton:pressed { background: #ff6b35; color: #12100e; }
            QLabel { color: #7a7068; }
        """)

        toolbar = self.addToolBar("Tools"); toolbar.setMovable(False); toolbar.setFloatable(False)

        # --- Element combo with keyboard shortcuts shown ---
        self.combo = QComboBox(); self.combo.setFixedWidth(180)
        cg = ""
        sep_indices = []
        idx = 0
        # Build list of selectable element indices for Tab cycling
        self._selectable_indices = []
        for el in ELEMS:
            if el["group"] != cg:
                self.combo.addItem(f"--- {el['group']} ---")
                sep_indices.append(idx)
                cg = el["group"]
                idx += 1
            # Show keyboard shortcut in the name
            display = el["name"]
            if el["key"]:
                display = f"{el['name']}  [{el['key']}]"
            self.combo.addItem(display, el["id"])
            self._selectable_indices.append(idx)
            idx += 1
        # Disable separator items so they can't be selected
        model = self.combo.model()
        for si in sep_indices:
            item = model.item(si)
            if item:
                item.setFlags(item.flags() & ~(Qt.ItemIsSelectable | Qt.ItemIsEnabled))
        self.combo.setCurrentIndex(3)
        self.combo.currentIndexChanged.connect(self._on_element_selected)
        toolbar.addWidget(self.combo)

        toolbar.addSeparator()
        toolbar.addWidget(QLabel("Brush:"))
        self.brush_slider = QSlider(Qt.Horizontal); self.brush_slider.setRange(1, 14); self.brush_slider.setValue(4); self.brush_slider.setFixedWidth(70)
        toolbar.addWidget(self.brush_slider)
        self.brush_label = QLabel(" 4 "); self.brush_label.setStyleSheet("color: #ff6b35; font-weight: bold;")
        self.brush_slider.valueChanged.connect(self._on_brush_changed)
        toolbar.addWidget(self.brush_label)

        toolbar.addSeparator()
        toolbar.addWidget(QLabel("Speed:"))
        self.speed_slider = QSlider(Qt.Horizontal); self.speed_slider.setRange(1, 5); self.speed_slider.setValue(1); self.speed_slider.setFixedWidth(50)
        self.speed_slider.valueChanged.connect(lambda v: setattr(self.gl_widget.sim, 'sim_speed', v))
        toolbar.addWidget(self.speed_slider)

        toolbar.addSeparator()
        toolbar.addWidget(QLabel("Bloom:"))
        self.bloom_slider = QSlider(Qt.Horizontal); self.bloom_slider.setRange(0, 20); self.bloom_slider.setValue(7); self.bloom_slider.setFixedWidth(60)
        self.bloom_slider.valueChanged.connect(lambda v: setattr(self.gl_widget, 'bloom_intensity', v / 10.0))
        toolbar.addWidget(self.bloom_slider)

        toolbar.addSeparator()
        btn_clear = QPushButton("Clear"); btn_clear.clicked.connect(self._clear_canvas)
        toolbar.addWidget(btn_clear)
        self.btn_pause = QPushButton("Pause"); self.btn_pause.clicked.connect(self.toggle_pause)
        toolbar.addWidget(self.btn_pause)
        btn_undo = QPushButton("Undo"); btn_undo.clicked.connect(self._do_undo)
        btn_undo.setToolTip("Ctrl+Z")
        toolbar.addWidget(btn_undo)
        btn_save = QPushButton("Save"); btn_save.clicked.connect(self._save_state)
        btn_save.setToolTip("Ctrl+S")
        toolbar.addWidget(btn_save)
        btn_load = QPushButton("Load"); btn_load.clicked.connect(self._load_state)
        btn_load.setToolTip("Ctrl+L")
        toolbar.addWidget(btn_load)

        toolbar.addSeparator()
        self.stats_label = QLabel("0 particles | 0 FPS")
        self.stats_label.setStyleSheet("color: #e8ddd0; font-size: 11px;")
        self.stats_label.setToolTip(
            "LClick: Draw | RClick: Erase | MClick: Pick element\n"
            "Scroll: Brush size | DblClick: Flood fill\n"
            "Shift+Click: Straight line mode\n"
            "Space: Pause | C: Clear | [ ]: Brush size\n"
            "Tab/Shift+Tab: Cycle elements | Ctrl+Z: Undo\n"
            "Ctrl+S: Save | Ctrl+L: Load\n"
            "Keys: 0-9, G, T, E, H, I, P, F, D, N, S, V, M, L, O, B, R"
        )
        toolbar.addWidget(self.stats_label)

        toolbar.addSeparator()
        self.hover_label = QLabel("")
        self.hover_label.setStyleSheet("color: #ff6b35; font-size: 11px; min-width: 140px;")
        self.hover_label.setToolTip("Element under cursor")
        toolbar.addWidget(self.hover_label)

        # Undo count label
        self.undo_label = QLabel("")
        self.undo_label.setStyleSheet("color: #7a7068; font-size: 10px; min-width: 50px;")
        toolbar.addWidget(self.undo_label)

        self.gl_widget = SandGLWidget()
        self.setCentralWidget(self.gl_widget)

        # Periodic undo count update
        self._ui_timer = QTimer(self)
        self._ui_timer.timeout.connect(self._update_ui_info)
        self._ui_timer.start(250)

    def _update_ui_info(self):
        """Periodically update undo count display."""
        try:
            n = len(self.gl_widget.sim._undo_stack)
            self.undo_label.setText(f"Undo: {n}")
        except Exception:
            pass

    def _on_element_selected(self, i):
        self.gl_widget.sim.selected_type = self.combo.itemData(i) or 0

    def _on_brush_changed(self, v):
        self.gl_widget.sim.brush_size = v
        self.brush_label.setText(f" {v} ")

    def _clear_canvas(self):
        sim = self.gl_widget.sim
        sim.save_snapshot()
        sim.grid.fill(0); sim.color_var.fill(0); sim.life.fill(0); sim.moved.fill(0)
        sim.push_undo()

    def _do_undo(self):
        if self.gl_widget.sim.undo():
            self.hover_label.setText("Undo!")

    def _save_state(self):
        """Save simulation state to a binary file."""
        sim = self.gl_widget.sim
        try:
            import pickle
            path = "/home/z/my-project/download/sand_save.pkl"
            data = {
                'grid': sim.grid.copy(),
                'color_var': sim.color_var.copy(),
                'life': sim.life.copy(),
                'W': sim.W, 'H': sim.H,
            }
            with open(path, 'wb') as f:
                pickle.dump(data, f)
            self.hover_label.setText(f"Saved!")
        except Exception as e:
            self.hover_label.setText(f"Save failed: {e}")

    def _load_state(self):
        """Load simulation state from a binary file."""
        sim = self.gl_widget.sim
        try:
            import pickle
            path = "/home/z/my-project/download/sand_save.pkl"
            with open(path, 'rb') as f:
                data = pickle.load(f)
            if data['W'] == sim.W and data['H'] == sim.H:
                sim.save_snapshot()
                sim.grid[:] = data['grid']
                sim.color_var[:] = data['color_var']
                sim.life[:] = data['life']
                sim.push_undo()
                self.hover_label.setText("Loaded!")
            else:
                self.hover_label.setText("Load: size mismatch!")
        except FileNotFoundError:
            self.hover_label.setText("No save file found")
        except Exception as e:
            self.hover_label.setText(f"Load failed: {e}")

    def closeEvent(self, event):
        """Clean up GPU resources before the GL context is destroyed."""
        try:
            self.gl_widget.makeCurrent()
            self.gl_widget._renderer.cleanup()
        except Exception:
            pass
        super().closeEvent(event)

    def toggle_pause(self):
        if self.gl_widget._sim_timer.isActive():
            self.gl_widget._sim_timer.stop()
            self.gl_widget._render_timer.stop()
            self.btn_pause.setText("Play")
        else:
            self.gl_widget._sim_timer.start(16)
            self.gl_widget._render_timer.start(16)
            self.btn_pause.setText("Pause")

    def _select_element(self, elem_id):
        """Select element by ID, updating the combo box."""
        for i in range(self.combo.count()):
            if self.combo.itemData(i) == elem_id:
                self.combo.setCurrentIndex(i)
                return

    def _cycle_element(self, direction=1):
        """Cycle through selectable elements (Tab/Shift+Tab)."""
        current = self.combo.currentIndex()
        sel = self._selectable_indices
        if not sel:
            return
        # Find current position in selectable list
        try:
            pos = sel.index(current)
        except ValueError:
            pos = 0
        pos = (pos + direction) % len(sel)
        self.combo.setCurrentIndex(sel[pos])

    def keyPressEvent(self, event):
        k = event.key()
        text = event.text().upper()
        modifiers = event.modifiers()

        # Ctrl+Z: Undo
        if modifiers & Qt.ControlModifier and k == Qt.Key_Z:
            self._do_undo(); return
        # Ctrl+S: Save
        if modifiers & Qt.ControlModifier and k == Qt.Key_S:
            self._save_state(); return
        # Ctrl+L: Load
        if modifiers & Qt.ControlModifier and k == Qt.Key_L:
            self._load_state(); return
        # Tab: Cycle elements
        if k == Qt.Key_Tab:
            direction = -1 if modifiers & Qt.ShiftModifier else 1
            self._cycle_element(direction); return
        # Escape: Cancel line anchor or deselect
        if k == Qt.Key_Escape:
            self.gl_widget.sim._line_anchor = None
            self.gl_widget._line_preview_end = None
            self.hover_label.setText("")
            return

        # Numeric keys 0-9: use the key field in ELEMS for direct mapping
        if Qt.Key_0 <= k <= Qt.Key_9:
            key_str = str(k - Qt.Key_0)
            for el in ELEMS:
                if el["key"] == key_str:
                    self._select_element(el["id"]); return
        # Letter-based shortcuts
        elif text and text.isalpha():
            if text == "C":
                self._clear_canvas(); return
            for el in ELEMS:
                if el["key"] == text:
                    self._select_element(el["id"]); return
            return  # letter key handled, don't fall through
        # Special keys
        if k == Qt.Key_Space: self.toggle_pause()
        elif k == Qt.Key_BracketLeft: self.brush_slider.setValue(self.brush_slider.value() - 1)
        elif k == Qt.Key_BracketRight: self.brush_slider.setValue(self.brush_slider.value() + 1)

if __name__ == "__main__":
    fmt = QSurfaceFormat()
    fmt.setVersion(4, 6)
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    fmt.setRenderableType(QSurfaceFormat.RenderableType.OpenGL)
    fmt.setDepthBufferSize(0)
    fmt.setStencilBufferSize(0)
    fmt.setSwapInterval(0)
    QSurfaceFormat.setDefaultFormat(fmt)
    app = QApplication(sys.argv)
    window = MainWindow(); window.show()
    sys.exit(app.exec())
