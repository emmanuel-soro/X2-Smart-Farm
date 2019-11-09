package ar.edu.soa.smartfarm;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;

public class MainActivity extends AppCompatActivity {

    ImageButton boton_nosotros;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        boton_nosotros = (ImageButton) findViewById(R.id.btnNosotros);

        boton_nosotros.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {

                Intent nosotrosIntent = new Intent(MainActivity.this, NosotrosActivity.class);
                startActivity(nosotrosIntent);
            }
        });
    }
}