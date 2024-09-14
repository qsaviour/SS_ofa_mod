using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using UAssetAPI;
using UAssetAPI.ExportTypes;
using UAssetAPI.PropertyTypes.Objects;
using UAssetAPI.PropertyTypes.Structs;
using UAssetAPI.UnrealTypes;


namespace UAssetEditPro
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // Write Lipsync

            int[] ss_i_map = { 0, 10, 6, 12, 13, 11, 14 };
            string base_folder = "E:\\IMModels\\ModProject\\Dance\\Song_bnd";
            //string ofa_string = File.ReadAllText("E:\\IMModels\\ModProject\\Dance\\Song_Cng\\lip\\ss\\LipSync_Sng026_00_ofa_target");
            string ofa_string = File.ReadAllText(base_folder + "\\lip\\ss\\LipSync_Sng026_00_ofa_target");
            float[][] ofalips = JsonConvert.DeserializeObject<float[][]>(ofa_string);

            UAsset myAsset = new UAsset(base_folder + "\\lip\\ss\\LipSync_Sng026_00.uasset", EngineVersion.VER_UE4_24);
            NormalExport myExport = (NormalExport)myAsset.Exports[0];
            var property = (ArrayPropertyData)myExport.Data[0];

            for(int i =0;i<property.Value.Length;i++)
            {
                var v = (StructPropertyData)property.Value[i];
                var vv = ((ArrayPropertyData)v.Value[0]).Value;
                for (int j = 0; j < vv.Length; j++)
                {
                    var vvv = (FloatPropertyData)(vv[j]);
                    if (i < ofalips.Length)
                    {
                        vvv.Value = ofalips[i][j];
                    }
                    else
                    {
                        vvv.Value = 0f;
                    }
                }
            }
            myAsset.Write(base_folder + "\\lip\\ss\\LipSync_Sng026_00_new.uasset");
            Console.WriteLine("Finished");
            Console.ReadLine();
        }
    }
}
