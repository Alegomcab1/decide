from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

        
    def simple(self, options, seats):

        out = []

        for opt in options:

            out.append({
                **opt,
                'postproc': 0,
            })

        out.sort(key=lambda x: -x['votes'])

        numeroEscanyos = seats;
        numeroVotos = 0;

        for votes in out:
            numeroVotos= numeroVotos + votes['votes'];

        valor_escanyo = numeroVotos/numeroEscanyos;


    def sin_paridad(self, options):

        """
        Metodo que devolverá el resultado de las votaciones sin tener en 
        cuenta la paridad de las personas presentadas a la votación

        * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
        """

        out = []

        for opt in options:

            out.append({
                **opt,
                'paridad': [],
            })

        for i in out:

            escanyos = i['postproc']
            presentados = i['presentados']
            x = 0

            while escanyos > 0:
              
                i['paridad'].append(presentados[x])
                x = x + 1

                escanyos = escanyos - 1 

        return out

    def porcentaje_hombre_mujer(self, hombres, mujeres):
        
        """
        Metodo que devolverá:
            True: Si el porcentaje de hombres y mujeres está equilibrado entre 60%-40%
            False: En caso contrario

        Inputs: 
            hombres: Array con los hombres candidatos en la votación
            mujeres: Array con las mujeres candidatas en la votación
        """

        #Obtenemos el total de participantes y sus porcentajes según sexo
        total = len(hombres) + len(mujeres)
        porcentaje_hombres = len(hombres)/total
        porcentaje_mujeres = len(mujeres)/total

        #Si se cumplen las estadísticas determinadas devolveremos True, en caso contrario, False
        if (porcentaje_hombres < 0.4) | (porcentaje_mujeres < 0.4):
            return False
        else:
            return True


    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT | SIN_PARIDAD
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        typeOfData = request.data.get('type')
        options =  request.data.get('options', [])

        if typeOfData == 'IDENTITY':
            return self.identity(options)

        elif typeOfData == 'SIN_PARIDAD':    
            
            return Response(self.sin_paridad(options))
           
        return Response({})
