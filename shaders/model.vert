#version 410 compatibility

layout(location = 0) in vec3 vertexPosition;
layout(location = 1) in vec4 vertexColor;
layout(location = 2) in vec2 vertexUV;
layout(location = 3) in vec4 vertexNormal;

out vec3 fragPos;
out vec4 fragColor;
out vec2 fragUV;
out vec4 fragNormal;

uniform mat4 camera;

void main()
{
    gl_Position = camera * vec4(vertexPosition, 1.0);

	fragPos = vertexPosition;
    fragColor = vertexColor;
	fragUV = vertexUV;
	fragNormal = vertexNormal;
}