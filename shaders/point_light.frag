#version 330

in vec4 fragColor;
in vec2 fragUV;
in vec3 fragNormal;

out vec4 outColor;

uniform vec3 lightDir;
uniform vec4 lightColor;
uniform float lightIntensity;

uniform sampler2D tex1;

void main()
{
	vec4 texVal = texture(tex1, fragUV);

	// simple lambert diffuse shading model
	float nDotL = max(dot(fragNormal, normalize(lightDir)), 0.0);
	outColor = fragColor * texVal * lightColor * lightIntensity * nDotL;
}