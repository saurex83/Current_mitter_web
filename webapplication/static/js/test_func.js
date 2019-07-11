function getRandomArbitrary(min, max) 
{
	return Math.random() * (max - min) + min;
}
	
function getSinus(x,a)
{
	return 50+(a+7*Math.random())*Math.sin(x/20)
}

function getSinus_shift(x,a,s)
{
	return 50+(a+7*Math.random())*Math.sin(x/20)+s
}