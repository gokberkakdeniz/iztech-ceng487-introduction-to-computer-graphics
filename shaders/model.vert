#version 410 compatibility

layout(location = 0) in vec3 vertexPosition;
layout(location = 1) in vec4 vertexColor;

out vec4 fragColor;

uniform mat4 camera;

void main()
{
   gl_Position = camera * vec4(vertexPosition, 1.0);
   fragColor = vertexColor;
}