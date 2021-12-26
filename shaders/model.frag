#version 330

in vec4 fragColor;
in vec2 fragUV;
in vec4 fragNormal;

out vec4 outColor;

uniform sampler2D tex1;

void main()
{
    vec4 texVal = texture(tex1, fragUV);

    outColor = fragColor * texVal;
}