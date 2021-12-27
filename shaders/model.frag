#version 330

in vec3 fragPos;
in vec4 fragColor;
in vec2 fragUV;
in vec4 fragNormal;

out vec4 outColor;

uniform float texBlendRatio;
uniform sampler2D tex1;
uniform sampler2D tex2;

uniform vec3 pointLight1Pos;
uniform vec4 pointLight1Color;
uniform float pointLight1Intensity;

uniform vec3 dirLight1Dir;
uniform vec4 dirLight1Color;
uniform float dirLight1Intensity;
uniform vec3 viewPos;
uniform bool blinEnabled;

void main()
{
    vec4 texVal1 = texture(tex1, fragUV);
    texVal1.a = texBlendRatio;
    
    vec4 texVal2 = texture(tex2, fragUV);
    texVal2.a = 1.0 - texBlendRatio;
    
    // vec4 texBlendVal = (1.0 - texVal1.a) * texVal2 + texVal1.a * texVal1;
    vec4 texBlendVal = mix(texVal1, texVal2, texVal2.a);

	vec4 pointLight1Dir = normalize(vec4(pointLight1Pos - fragPos, 1.0));
	float pointLight1nDotL = max(dot(fragNormal, pointLight1Dir), 0.0);
    vec4 pointLight1 = pointLight1Color * pointLight1Intensity * pointLight1nDotL;

	float dirLight1nDotL = max(dot(fragNormal, normalize(vec4(dirLight1Dir, 0.0))), 0.0);
    vec4 dirLight1 = dirLight1Color * dirLight1Intensity * dirLight1nDotL;


    float pointLight1Spec = 1.0;
    float dirLight1Spec = 1.0;

    if (blinEnabled) {
        vec4 viewDir = normalize(vec4(viewPos - fragPos, 1.0));

        vec4 pointLight1halfwayDir = normalize(pointLight1Dir + viewDir);  
        pointLight1Spec = pow(max(dot(fragNormal, pointLight1halfwayDir), 0.0), 4.0);

        vec4 dirLight1halfwayDir = normalize(vec4(dirLight1Dir, 0.0) + viewDir);  
        dirLight1Spec = pow(max(dot(fragNormal, dirLight1halfwayDir), 0.0), 0.5);
    }

    vec4 lightVal = dirLight1 * dirLight1Spec + pointLight1 * pointLight1Spec;

    outColor = fragColor * texBlendVal * lightVal;
}