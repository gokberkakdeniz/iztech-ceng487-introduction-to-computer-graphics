#version 410 compatibility

layout(location = 0) in vec3 vertexPosition;
layout(location = 1) in vec4 vertexColor;
layout(location = 2) in vec2 vertexUV;
layout(location = 3) in vec4 vertexNormal;

out vec3 fragPos;
out vec4 fragColor;
out vec2 fragUV;
out vec4 fragNormal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(vertexPosition, 1.0);

	fragPos = vec3(model * vec4(vertexPosition, 1.0));
    fragColor = vertexColor;
	fragUV = vertexUV;
	fragNormal = normalize(transpose(inverse(model)) * vertexNormal);
}