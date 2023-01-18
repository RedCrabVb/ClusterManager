import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { InitFilePage } from './page/initfile/initfile.page.component';
import { WelcomeComponent } from './page/welcome/welcom.page.component';

const routes: Routes = [
  // {
    // 'path': '**', component: AppComponent
  // }, 
  {
    'path': 'initfile', component: InitFilePage
  },
  {
    'path': 'welcome', component: WelcomeComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
